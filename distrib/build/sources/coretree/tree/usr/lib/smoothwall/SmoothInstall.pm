#!/usr/bin/perl 
###########################################
# SmoothInstall
#
# $Id: SmoothInstall.pm 592 2011-01-27 10:52:00Z steve@domesticsecurity.com.au $
#
###########################################

###########################################
package SmoothInstall;
our $VERSION    = "1.35";
###########################################
use lib "/var/smoothwall/mods/SmoothInstall/lib/perl5";
use warnings;
require Exporter;

our $RED = "\033[31;1m";
our $GREEN = "\033[32;1m";
our $CYAN = "\033[36;1m";
our $PURPLE = "\033[35;1m";
our $YELLOW = "\033[33;1m";
our $NORMAL = "\033[m";
our $RHS = "\033[80`";
our %ModDetails;

@ISA = qw(Exporter);
@EXPORT         = qw();
@EXPORT_OK      = qw( InsertBefore InsertAfter Prepend Append Change CommentOut Remove Start Stop Restart Status Running StartMod StopMod Init Untar INFO $RED $GREEN $CYAN $PURPLE $YELLOW $NORMAL $MODDIR PRINT ClearScreen %ModDetails);

%EXPORT_TAGS    = (
                standard   => [@EXPORT_OK],
                );


$|=1; # line buffering

use lib "/usr/lib/smoothwall";
use Log::Log4perl qw(:easy);
use Config::Patch;
use Archive::Tar;
use App::Control;
use header  qw( :standard );
use File::Basename;


###########################################
sub InsertBefore {
###########################################
	my ($file, $key, $pattern, @data) = @_;
	if ( -e $file) {
		my $data = join("\n", @data);
		my $patcher = Config::Patch->new(
			file => $file,
		);
		$patcher->eject( $key );
		my $hunk = Config::Patch::Hunk->new(
			key  => $key,
			mode => "insert-before",
			regex => qr($pattern)sm,
			text => $data
		);
		$patcher->apply( $hunk );
		$patcher->save();
	
		$data = join(" ", @data);
		INFO("InsertBefore {$file} {$key} {$pattern} {$data}");
	} 
	else {
		PRINT("${RED}InsertBefore: ERROR - File $file Does Not Exist${NORMAL}");
	}

}

###########################################
sub Prepend {
###########################################
	my ($file, $key, @data) = @_;
	if ( -e $file) {
		my $data = join("\n", @data);
		$data .= "\n";
		my $patcher = Config::Patch->new(
			file => $file,
		);
		$patcher->eject( $key );
		my $hunk = Config::Patch::Hunk->new(
			key  => $key,
			mode => "prepend",
			text => $data
		);
		$patcher->apply( $hunk );
		$patcher->save();
	
		$data = join(" ", @data);
		INFO("Prepend {$file} {$key} {$data}");
	} 
	else {
		PRINT("${RED}Prepend: ERROR - File $file Does Not Exist${NORMAL}");
	}
}

###########################################
sub Append {
###########################################
	my ($file, $key, @data) = @_;
	if ( -e $file) {
		my $data = join("\n", @data);
		$data .= "\n";
		my $patcher = Config::Patch->new(
			file => $file,
		);
		$patcher->eject( $key );
		my $hunk = Config::Patch::Hunk->new(
			key  => $key,
			mode => "append",
			text => $data
		);
		$patcher->apply( $hunk );
		$patcher->save();
	
		$data = join(" ", @data);
		INFO("Append {$file} {$key} {$data}");
	} 
	else {
		PRINT("${RED}Append: ERROR - File $file Does Not Exist${NORMAL}");
	}
}

###########################################
sub InsertAfter {
###########################################
	my ($file, $key, $pattern, @data) = @_;
	if ( -e $file) {
                my $data = join("\n", @data);
                my $patcher = Config::Patch->new(
                        file => $file,
                );
                $patcher->eject( $key );
                my $hunk = Config::Patch::Hunk->new(
                        key  => $key,
                        mode => "insert-after",
                        regex => qr($pattern)sm,
                        text => $data
                );
                $patcher->apply( $hunk );
                $patcher->save();

		$data = join(" ", @data);
		INFO("InsertAfter {$file} {$key} {$pattern} {$data}");
	}
	else {
		PRINT("${RED}InsertAfter: ERROR - File $file Does Not Exist${NORMAL}");
	}
}

###########################################
sub Change {
###########################################
	my ($file, $key, $pattern, @data) = @_;
	if ( -e $file) {
                my $data = join("\n", @data);
                my $patcher = Config::Patch->new(
                        file => $file,
                );
                $patcher->eject( $key );
                my $hunk = Config::Patch::Hunk->new(
                        key  => $key,
                        mode => "replace",
                        regex => qr($pattern)sm,
                        text => $data
                );
                $patcher->apply( $hunk );
                $patcher->save();
	
		$data = join(" ", @data);
		INFO("Change {$file} {$key} {$pattern} {$data}");
	}
	else {
		PRINT("${RED}Change: ERROR - File $file Does Not Exist${NORMAL}");
	}
}

###########################################
sub CommentOut {
###########################################
	my ($file, $key, $pattern) = @_;
	if ( -e $file) {
                my $data = join("\n", @data);
                my $patcher = Config::Patch->new(
                        file => $file,
                );
                $patcher->eject( $key );
                my $hunk = Config::Patch::Hunk->new(
                        key  => $key,
                        mode => "replace",
                        regex => qr($pattern)sm,
                        text => ''
                );
                $patcher->apply( $hunk );
                $patcher->save();

		INFO("CommentOut {$file} {$key} {$pattern}");
	}
	else {
		PRINT("${RED}CommentOut: ERROR - File $file Does Not Exist${NORMAL}");
	}
}

###########################################
sub Remove {
###########################################
	my ($file, $key) = @_;
	if ( -e $file) {
                my $patcher = Config::Patch->new(
                        file => $file,
                );
                $patcher->eject( $key );
		$patcher->save();

		INFO("Remove {$file} {$key}");
	}
	else {
		PRINT("${RED}Remove: ERROR - File $file Does Not Exist${NORMAL}");
	}
}

###########################################
sub Start {
###########################################
	my ($exec, @args) = @_;
	my $pid = $exec;
	my $cwd = `pwd`;
	chdir("/tmp");
	$pid =~ s/^(.*\/)//;
	$pid = "/var/run/" . $pid . ".pid";
        my $ctl = App::Control->new(
                EXEC => $exec,
                ARGS => \@args,
                PIDFILE => $pid,
                SLEEP => 1,
                LOOP => 6,
                VERBOSE => 0,
        );
        $ctl->start;
	my $status = $ctl->running;
	chomp $status;
	my $args = join(" ", @args);
	INFO("Start {$exec} {$status}");
	chdir ($cwd);
	return $status;	
}

###########################################
sub Stop {
###########################################
	my ($exec, @args) = @_;
	my $pid = $exec;
	$pid =~ s/^(.*\/)//;
	$pid = "/var/run/" . $pid . ".pid";
        my $ctl = App::Control->new(
                EXEC => $exec,
                ARGS => \@args,
                PIDFILE => $pid,
                SLEEP => 1,
                LOOP => 6,
                VERBOSE => 0,
        );
        $ctl->stop;
	my $status = $ctl->running;
	chomp $status;
	my $args = join(" ", @args);
	INFO("Stop {$exec} {$status}");
	return $status;	
}

###########################################
sub Restart {
###########################################
	&Stop(@_);
	&Start(@_);
}

###########################################
sub Status {
###########################################
	my ($exec, @args) = @_;
	my $pid = $exec;
	$pid =~ s/^(.*\/)//;
	$pid = "/var/run/" . $pid . ".pid";
       	my $ctl = App::Control->new(
               	EXEC => $exec,
                ARGS => \@args,
       	        PIDFILE => $pid,
               	SLEEP => 1,
                LOOP => 6,
       	        VERBOSE => 0,
	        );
	my $status = $ctl->running;
	chomp $status;
	my $args = join(" ", @args);
	INFO("Status {$exec} {$status}");
	return $status;	
}

###########################################
sub Running {
###########################################
	my ($exec, @args) = @_;
	if (-e $exec) {
		my $status = &Status(@_);
		if ($status ne "0") {
			return("True");
		}
		else {
			return
		}
	}
}

###########################################
sub StopMod {
###########################################
	my ($Binary, $Mod) = @_;
	my $running = &Running($Binary);
	if ($running) {
	        print $NORMAL . "Stopping $Mod to facilitate installation update $NORMAL";
	        my $status = &Stop($Binary);
	        if ($status eq "0") {
	                print "$GREEN $RHS [OK] $NORMAL\n"; INFO "Stopping $Mod to facilitate installation update (OK)";
	        }
	        else {
        	        print "$RED $RHS [FAILED] $NORMAL\n"; INFO "Stopping $Mod to facilitate installation update [FAILED] ($!)";
	        }
		return $running;
	}
	else {
		print $RED . "$Mod Not Running" . $NORMAL . "\n"; INFO "$Mod Not Running";
		return undef $running;
	}
}

###########################################
sub StartMod {
###########################################
	my ($Binary, $Mod, @Args) = @_;
        print $NORMAL . "Attempting to Start $Mod $NORMAL";
        my $status = &Start($Binary, @Args);
        if ($status eq "1") {
                print "$GREEN $RHS [OK] $NORMAL\n"; INFO "Attempting to Start $Mod (OK)";
        }
        else {
       	        print "$RED $RHS [FAILED] $NORMAL\n"; INFO "Attempting to Start $Mod [FAILED] ($!)";
        }
}

###########################################
sub Init {
###########################################
	my $modname = $_[0];
	our $MODDIR = "/var/smoothwall/mods/$modname";
	&readhash( "$MODDIR/DETAILS", \%ModDetails );
	if (!($ENV{'SCRIPT_NAME'})) {
		my $logtype = File::Basename::basename($0);
		$logtype =~ s/.pl//g;
		my $logfilename = "/tmp/$ModDetails{'MOD_NAME'}-$logtype.log";

		Log::Log4perl->easy_init( { file    => $logfilename,
	       				    level   => $INFO	} );
	        $SIG{'__WARN__'} = sub { &INFO("WARNING: $_[0]") };
		INFO("NOTE: ERRORS CONCERNING SYMBOLIC LINKS ARE NORMAL");
	}
}

###########################################
sub PRINT {
###########################################
	print "@_\n";
	foreach my $line (@_) {
		$line =~ s/\n//g;
		$line =~ s/\033//g;
		$line =~ s/\Q[31;1m\E|\Q[32;1m\E|\Q[36;1m\E|\Q[35;1m\E|\Q[m\E|\Q[80`\E//g;
		INFO($line) ;
	}
}

###########################################
sub ClearScreen {
###########################################
	system("tput clear");
}

###########################################
sub Untar {
###########################################
        my $archive = $_[0];
        my $overwrite = $_[1];

        my $tar = Archive::Tar->new;
        $tar->read("$archive",1);
	#$tar->error(1);
        my @items = $tar->get_files;
        foreach my $item (@items) {
                my $filename = "/" . $item->name;
                my $archivefile = $item->name;
                my $archivetime = $item->mtime;
                my ($dev,$ino,$mode,$nlink,$uid,$gid,$rdev,$size,$atime,$mtime,$ctime,$blksize,$blocks)= stat($filename);
                if (-e $filename) {
                                if (!($overwrite)) {
                                        if ($archivetime gt $mtime) {
                                                INFO("Updating $filename");
                                                $tar->extract_file($archivefile, $filename);
                                        }
                                }
                                else {
                                        INFO("Installing $filename");
                                        $tar->extract_file($archivefile, $filename);
                                }
                }
                else {
                        INFO("Installing $filename");
                        $tar->extract_file($archivefile, $filename);
                }
        }

}

1;

