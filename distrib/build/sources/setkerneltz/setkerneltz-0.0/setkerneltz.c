/*
    setsystz: set the Linux kernel's idea of the time zone
    David A. Madore <david.madore@xxxxxx>, 2007-02-19. Public Domain

    Rationale: the Linux kernel needs to have some idea of time zone, notably
    because some filesystems (e.g. FAT) store file modification/access times
    in local time rather than UTC(=GMT) (which Unix uses internally for all
    timestamps). This kernel (system) time zone is set through the
    settimeofday() system call; unfortunately, there does not seem to be a
    practical way to do it, and some (all?) Linux distributions get it wrong:
    e.g., simply because my CMOS clock is set to GMT (as recommended), my
    Debian init scripts apparently assume that any FAT filesystems I'll be
    mounting will have GMT timestamps (uh?). Note: IMHO, the whole idea of
    having a per-system global time zone is probably wrong, and FAT mounts
    should probably better use an adhoc option to specify GMT offset
    (defaulting to the libc time zone for the mount process), and CMOS clock
    thingies should be kept separate.

    What this does: called without arguments, setsystz sets the kernel's time
    zone to the userland's time zone (typically from the /etc/localtime file,
    overridden by the TZ environment variable if it exists). With an explicit
    argument, setsystz sets the kernel's time zone to that many minutes west
    of GMT (see settimeofday(2) man page for explanations). This program takes
    care _not_ to change/warp the system clock while changing the time zone:
    see comments on avoid_linux_braindeadness() below.

    How to use: probably just call "setsystz" (as root) before mounting a FAT
    filesystem, if the files it contains are in your usual system time zone.
    If they are, e.g., from the Shanghai time zone, then use "TZ=Asia/Shanghai
    setsystz" before mounting. Note: it's probably wiser not to do this while
    there are existing mounted FAT filesystems.
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>



/*
    Determine localtime GMT offset and return it in minutes west of GMT (as
    expected by a struct timezone). This will typically use the TZ environment
    variable if it is defined or, as a fallback, the contents of
    /etc/localtime (see libc documentation for more details).
*/

int
auto_minutes (void)
{
    time_t now = time(NULL);
    struct tm *lt = localtime (&now);
    long int gmtoff = lt->tm_gmtoff;

    fprintf (stderr, "GMT offset=%lds\n", gmtoff);
    if ( gmtoff%60 )
    {
        fprintf (stderr,
                 "warning: GMT offset %lds is not an integer number of minutes\n",
                 gmtoff);
    }
    gmtoff /= 60;
    return -gmtoff;
}



/*
    We ___DO NOT___ want to change the system time, only the
    system time zone! Since Linux does something special
    (warp_clock() semantics) the very first time settimeofday() is
    called with tz!=NULL, we call it once with tz pointing to a
    GMT-filled structure, i.e., tz->tz_minuteswest==0 (so the
    clock won't be warped). The settimeofday(2) man page claims
    that tz->tz_minuteswest==0 will not count toward cancelling
    the warp_clock() semantics, i.e., that our trick does not
    work: fortunately, it is wrong (at least under 2.6.19 and
    whereabouts) and our trick works. Note however that this
    still resets the time interpolator the first time:
    unfortunately there does not seem to be a way around this
    problem. See /usr/src/linux/kernel/time.c for details
    about the whole mess. -- David A. Madore 2007-02-19
*/

void
avoid_linux_braindeadness (void)
{
    struct timezone tz;

    memset (&tz, 0, sizeof(struct timezone));
    tz.tz_minuteswest = 0;
    tz.tz_dsttime = 0;
    settimeofday (NULL, &tz);
}



int
main (int argc, char *argv[])
{
    int minuteswest;

    if ( argc == 1 )
        minuteswest = auto_minutes();
    else if ( argc == 2 )
    {
        if ( sscanf (argv[1], "%d", &minuteswest) != 1 )
        {
            fprintf (stderr, "invalid argument: %s\n", argv[1]);
            exit (2);
        }
    }
    else
    {
        fprintf (stderr, "wrong number or arguments\n");
        exit (2);
    }

    struct timezone tz;

    memset (&tz, 0, sizeof(struct timezone));
    tz.tz_minuteswest = minuteswest;
    tz.tz_dsttime = 0;
    fprintf (stderr, "setting system time zone to tz_minuteswest=%d\n", minuteswest);

#if 1
    avoid_linux_braindeadness ();

    if ( settimeofday (NULL, &tz) == -1 )
    {
        perror ("settimeofday()");
        exit (EXIT_FAILURE);
    }
#endif

    return 0;
}

