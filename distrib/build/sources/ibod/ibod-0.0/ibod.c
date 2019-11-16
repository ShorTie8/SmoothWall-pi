static char *rcsId = "$Id$";
static char *rcsSymbol = "$Symbol$";

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <signal.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <linux/isdn.h>
#include <syslog.h>
#include <errno.h>
#include "ibod.h"

static int setattr(char *home);
static void reread(int sig);
static void pipehndl(int sig);
static void setinterval();
static void get_if_state();
static int bring_up_slave();
static int bring_down_slave();
static char *home;
static Conf cf;
static struct timeval timeout, tv_last, tv_up;
static int usageflags[ISDN_MAX_CHANNELS];
static char phone[ISDN_MAX_CHANNELS][20];
static Siobytes iobytes[ISDN_MAX_CHANNELS];
static unsigned long in_bytes_last, out_bytes_last;
static unsigned long in_bytes_per_sec, out_bytes_per_sec;
static unsigned long channels_last;
static int  channels_now;
static int  msgsock = -1;	/* Communication socket descriptor */


main(int argc, char *argv[])
{
    fd_set readfds, writefds, execptfds;
    int    s;			/* Listening socket descriptor */
    struct sockaddr_in server;	/* Socket protocol descriptor */
    char   buf[MAX_MSG_LEN];
    int    max_fd, rc;

    if (daemon(0, 0))
        fprintf(stderr, "daemon failed\n");

    openlog("ibod", LOG_PID, LOG_DAEMON);

    
       
    channels_last = -1;

    /* Find out where to look for configuration file */
    if ((home = getenv("IBOD_HOME")) == NULL)
        home = IBOD_DEFAULT_DIR;

    /* Setup initial attributes */
    if (setattr(home) == -1) {
        closelog();
        exit(1);
    }

    setinterval();

    /* Setup handlig of signal SIGHUP and SIGPIPE */
    signal(SIGHUP, reread);
    signal(SIGPIPE, pipehndl);

    /* Create a socket for control panel communication */
    if ((s = socket(PF_INET, SOCK_STREAM, 0)) == -1) {
        syslog(LOG_ERR, "creating socket: %s\n", sys_errlist[errno]);
        closelog();
        exit(1);
    }

    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons(IBOD_PORT);
    if (bind(s, (struct sockaddr *)&server, sizeof(struct sockaddr_in)) < 0) {
        syslog(LOG_ERR, "binding stream socket: %s\n", sys_errlist[errno]);
        closelog();
        exit(1);
    }

    /* Start accepting connections. */
    listen(s, 5);
    
    FD_ZERO(&readfds);
    FD_ZERO(&execptfds);

    do {
        setinterval();

        FD_SET(s, &readfds);
        FD_SET(s, &execptfds);
        if (msgsock > 0) {
            FD_SET(msgsock, &readfds);
            FD_SET(msgsock, &execptfds);
        }

        max_fd = s;
        if (msgsock > max_fd)
            max_fd = msgsock;

        if ((rc = select(max_fd + 1, &readfds, NULL, &execptfds, &timeout)) < 0) {
            syslog(LOG_ERR, "select: %s\n", sys_errlist[errno]);
            continue;
        }

        if (FD_ISSET(s, &readfds)) {
            msgsock = accept(s, (struct sockaddr *)0, (int *)0);
            if (msgsock == -1)
                syslog(LOG_ERR, "accept: %s\n", sys_errlist[errno]);
        }

        if (msgsock != -1 && FD_ISSET(msgsock, &readfds)) {
            int  rval;

            memset(buf, 0, sizeof buf);
            if ((rval = read(msgsock, buf, 1024)) < 0)
                syslog(LOG_ERR, "reading stream message: %s\n",
                       sys_errlist[errno]);
            else {
                int  cmd = *(int *)buf;

                switch (cmd) {
                    case CMD_OPEN:
                        break;

                    case CMD_CLOSE:
                        close(msgsock);
                        msgsock = -1;
                        break;
 
                    case CMD_UP2:
                        if (channels_now == 1) {
                            if (bring_up_slave() == -1)
                                exit(1);
                        }
                        break;

                    case CMD_DOWN2:
                        if (channels_now == 2) {
                            if (bring_down_slave() == -1)
                                exit(1);
                        }
                        break;

                    case CMD_ENABLE:
                        cf.enable = 1;
                        break;

                    case CMD_DISABLE:
                        if (channels_now == 2) {
                            if (bring_down_slave() == -1)
                                exit(1);
                        }

                        cf.enable = 0;
                }
            }
        }

        if (FD_ISSET(s, &execptfds)) {
           perror("Exception on s");
        }

        if (msgsock != -1 && FD_ISSET(msgsock, &execptfds)) {
           perror("Exception on msgsock");
           FD_SET(msgsock, &execptfds);
        }
        if (1) {

            /* Gate state of interface */
            get_if_state();

            if (msgsock > 0) {
                memcpy(&buf[LINK_STATUS_POS], &channels_now, POBJ_SIZE);
                memcpy(&buf[INBOUND_RATE_POS], &in_bytes_per_sec, POBJ_SIZE);
                memcpy(&buf[OUTBOUND_RATE_POS], &out_bytes_per_sec, POBJ_SIZE);

                write(msgsock, buf, STATUS_FRAME_SIZE);
            }
        }

    } while (1);
}


static int setattr(char *home)
{
    FILE *fd;
    char config_filename[MAX_STR_LEN];
    char linebuf[MAX_STR_LEN];
    char *key, *value;
    int  val;

    strcpy(cf.dev, DEVICE);
    cf.enable      = ENABLE;
    cf.interval    = INTERVAL;
    cf.filter      = FILTER;
    cf.limit       = LIMIT;
    cf.stayup      = STAYUP;
    cf.stayup_time = STAYUP_TIME;

    /* Open config file */
    sprintf(config_filename, "%s/ibod.cf", home);
    if ((fd = fopen(config_filename, "r")) == NULL) {
        syslog(LOG_ERR, "%s: %s\n", config_filename, strerror(errno));
        return -1;
    }

    /* Loop over the config file to setup attributes */
    while (fgets(linebuf, MAX_STR_LEN, fd) != NULL) {

        if (*linebuf == '#')		/* Ignore comments */
            continue;

        key = strtok(linebuf, " \t");
        value = strtok(NULL, " \t\n");

        if (strcmp(key, "DEVICE") == 0) {
            if (strcmp(cf.dev, value) != 0)
                syslog(LOG_NOTICE,
                       "Parameter DEVICE reconfigured to %s\n", value);
            strcpy(cf.dev, value);
        }

        if (strcmp(key, "ENABLE") == 0) {
            val = atoi(value);
            if (cf.enable != val)
                syslog(LOG_NOTICE,
                       "Parameter ENABLE reconfigured to %d\n", val);
            cf.enable = val;
        }

        if (strcmp(key, "INTERVAL") == 0) {
            val = atoi(value);
            if (cf.interval != val)
                syslog(LOG_NOTICE,
                       "Parameter INTERVAL reconfigured to %d\n", val);
            cf.interval = atoi(value);
        }

        if (strcmp(key, "FILTER") == 0) {
            val = atoi(value);
            if (cf.filter != val)
                syslog(LOG_NOTICE,
                       "Parameter FILTER reconfigured to %d\n", val);
            cf.filter = atoi(value);
        }

        if (strcmp(key, "LIMIT") == 0) {
            val = atoi(value);
            if (cf.limit != val)
                syslog(LOG_NOTICE,
                       "Parameter LIMIT reconfigured to %d\n", val);
            cf.limit = atoi(value);
        }

        if (strcmp(key, "STAYUP") == 0) {
            val = atoi(value);
            if (cf.stayup != val)
                syslog(LOG_NOTICE,
                       "Parameter STAYUP reconfigured to %d\n", val);
            cf.stayup = atoi(value);
        }

        if (strcmp(key, "STAYUP_TIME") == 0) {
            val = atoi(value);
            if (cf.stayup_time != val)
                syslog(LOG_NOTICE,
                       "Parameter STAYUP_TIME reconfigured to %d\n", val);
            cf.stayup_time = atoi(value);
        }
    }

    fclose(fd);
    return 0;
}



static void setinterval()
{
    timeout.tv_sec = cf.interval / 1000;
    timeout.tv_usec = (cf.interval % 1000) * 1000;
}


static void reread(int sig)
{
    (void) setattr(home);

    setinterval();

    signal(SIGHUP, reread);
}


static void pipehndl(int sig)
{
    syslog(LOG_ERR, "caught SIGPIPE: %s\n", sys_errlist[errno]);

    close(msgsock);
    msgsock = -1;

    signal(SIGPIPE, pipehndl);
}


static void get_if_state()
{
    static char buf[4096];
    struct timeval tv_now;
    int    ms_delta;
    int    in_bytes_now, out_bytes_now;
    int  fd;
    int  i;

    /* Open the info device */
    if ((fd = open(ISDN_INFO_DEV, O_RDONLY | O_NDELAY)) < 0) {
        syslog(LOG_ERR, "%s: %s\n", ISDN_INFO_DEV, sys_errlist[errno]);
        closelog();
        exit(1);
    }

    /* Whats the time now */
    gettimeofday(&tv_now, NULL);
    ms_delta = (tv_now.tv_sec * 1000 + tv_now.tv_usec / 1000) -
               (tv_last.tv_sec * 1000 + tv_last.tv_usec / 1000);
    tv_last = tv_now;

    /* Get info from interface */
    if (read(fd, buf, sizeof(buf))> 0) {
        sscanf(strstr(buf, "usage:"),
            "usage: %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d",
            &usageflags[0], &usageflags[1], &usageflags[2], &usageflags[3],
            &usageflags[4], &usageflags[5], &usageflags[6], &usageflags[7],
            &usageflags[8], &usageflags[9], &usageflags[10], &usageflags[11],
            &usageflags[12], &usageflags[13], &usageflags[14], &usageflags[15]);
        sscanf(strstr(buf, "phone:"),
            "phone: %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s",
            phone[0], phone[1], phone[2], phone[3],
            phone[4], phone[5], phone[6], phone[7],
            phone[8], phone[8], phone[10], phone[11],
            phone[12], phone[13], phone[14], phone[15]);
    }

    in_bytes_now = 0;
    out_bytes_now = 0;
    channels_now = 0;

    /* Get byte in/out for all channels */
    if (ioctl(fd, IIOCGETCPS, &iobytes)) {
        syslog(LOG_ERR, "%s: %s\n", IIOCGETCPS, sys_errlist[errno]);
        closelog();
        exit(1);
    }
    close(fd);
          
    /* Count number of open channes and total in/out bytes */
    for (i = 0; i < ISDN_MAX_CHANNELS; i++) {
        if (usageflags[i]) {
            channels_now++;
            in_bytes_now += iobytes[i].ibytes;
            out_bytes_now += iobytes[i].obytes;
        }
    }

    if (channels_last == -1 || channels_now < channels_last) {
        channels_last = channels_now;
        in_bytes_last = in_bytes_now;
        out_bytes_last = out_bytes_now;
        return;
    }

    /* Calculate the total through put in bytes/sec */
    if (cf.filter < 1) {
        in_bytes_per_sec =
            (in_bytes_now - in_bytes_last) * 1000 / ms_delta;
        out_bytes_per_sec =
            (out_bytes_now - out_bytes_last) * 1000 / ms_delta;
    }
    else {
        in_bytes_per_sec = (in_bytes_per_sec * (cf.filter - 1) +
            (in_bytes_now - in_bytes_last) * 1000 / ms_delta) / cf.filter;
        out_bytes_per_sec = (out_bytes_per_sec * (cf.filter - 1) +
            (out_bytes_now - out_bytes_last) * 1000 / ms_delta) / cf.filter;
    }

    in_bytes_last = in_bytes_now;
    out_bytes_last = out_bytes_now;

    if (channels_now == 0) {
        channels_last = channels_now;
        return;
    }

    /* Take up or down slave channel */

    if (cf.enable == 0) {
        channels_last = channels_now;
        return;
    }

    if (channels_now == 1 &&
        (in_bytes_per_sec > cf.limit || out_bytes_per_sec >  cf.limit)) {

        /* Bring up slave interface */
        if (bring_up_slave() == -1)
            exit(1);

        /* Start stay up timer */
        gettimeofday(&tv_up, NULL);
    }

    if ((channels_now > 1) &&
        (in_bytes_per_sec <= cf.limit) &&
        (out_bytes_per_sec <= cf.limit) &&
        (cf.stayup == 0)) {

        /* Check that the min stay up timer has expired */
        gettimeofday(&tv_now, NULL);
        if (tv_now.tv_sec - tv_up.tv_sec > cf.stayup_time) {

            /* Bring down slave interface */
            if (bring_down_slave() == -1)
                exit(1);
        }
    }

    channels_last = channels_now;
}


static int bring_up_slave()
{
    int  fd, rc;

    if ((fd = open(ISDN_CTLR_DEV, O_RDWR)) < 0) {
        syslog(LOG_ERR, "%s: %s\n", ISDN_CTLR_DEV, sys_errlist[errno]);
        closelog();
        return -1;
    }

    if ((rc = ioctl(fd, IIOCNETALN, cf.dev)) < 0) {
        syslog(LOG_ERR, "%s: %s\n", cf.dev, sys_errlist[errno]);
        closelog();
        return -1;
    }

    close(fd);

    if (rc)
        syslog(LOG_NOTICE, "unable to attach additional link: %d\n", rc);
    else {
        syslog(LOG_NOTICE, "added new link\n");
        channels_now = 2;
    }

    return 0;
}


static int bring_down_slave()
{
    int  fd, rc;

    if ((fd = open(ISDN_CTLR_DEV, O_RDWR)) < 0) {
        syslog(LOG_ERR, "%s: %s\n", ISDN_CTLR_DEV, sys_errlist[errno]);
        closelog();
        return -1;
    }

    if ((rc = ioctl(fd, IIOCNETDLN, cf.dev)) < 0) {
        syslog(LOG_ERR, "%s: %s\n", cf.dev, sys_errlist[errno]);
        closelog();
        return -1;
    }

    close(fd);

    if (rc)
        syslog(LOG_ERR, "unable to remove additional link: %d\n", rc);
    else {
        syslog(LOG_NOTICE, "removed link\n");
    }

    return 0;
}
