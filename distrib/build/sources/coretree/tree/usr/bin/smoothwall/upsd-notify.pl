#!/usr/bin/perl
# Perl mail notification script for NUT mod by panda.

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use Net::SMTP;
use Net::SMTPS;
use strict;

my (%mailsettings, %hostsettings, @upsdata, $smtp, $upsdata, $TO, $CC, $SMS);
&readhash("${swroot}/apcupsd/settings", \%mailsettings);
&readhash("${swroot}/main/settings", \%hostsettings);
my $log = "${swroot}/apcupsd/events";
my $maildate = `date -R`; chomp $maildate;
my $logdate = `date -d '$maildate' '+%Y-%m-%d %T %z'`; chomp $logdate;
my $errfile = "/dev/shm/upsd-notify_failed";
my $logfile = "${swroot}/apcupsd/maillog";
open (STDERR, ">", "$logfile") or die "Can't open log";

@upsdata = `/sbin/apcaccess`;

my @upstimeleft = grep { /^TIMELEFT/ } @upsdata;
my @upsstatus = grep { /^STATUS/ } @upsdata;
my @upscharge = grep { /^BCHARGE/ } @upsdata;

if ($mailsettings{'ENABLEAUTH'} eq 'on') {
	if ($mailsettings{'SMTPS'} eq 'on' && $mailsettings{'STARTTLS'} ne 'on') {
		&send_mail_auth_smtps;
	}
	elsif ($mailsettings{'SMTPS'} ne 'on' && $mailsettings{'STARTTLS'} eq 'on') {
		&send_mail_starttls;
	}
	elsif ($mailsettings{'SMTPS'} ne 'on' && $mailsettings{'STARTTLS'} ne 'on') {
		&send_mail_auth;
	}
}
else {
	&send_mail;
}


sub send_mail {
	if (not $smtp = Net::SMTP->new($mailsettings{'SMTPSERVER'},
		Timeout => 60,
		Debug => 1,
		Port => $mailsettings{'PORT'})) {
			system ("/bin/touch", "$errfile"); die "Could not connect to $mailsettings{'SMTPSERVER'}: $!\n";
	}
	&common;
}

sub send_mail_auth {
	if (not $smtp = Net::SMTP->new($mailsettings{'SMTPSERVER'},
		Timeout => 60,
		Debug => 1,
		Port => $mailsettings{'PORT'})) {
			system ("/bin/touch", "$errfile"); die "Could not connect to $mailsettings{'SMTPSERVER'}: $!\n";
	}
	$smtp->auth( $mailsettings{'USER'}, $mailsettings{'EMAIL_PASSWORD'}) || die "Authentication failed!\n";
	&common;
}

sub send_mail_auth_smtps {
	if (not $smtp = Net::SMTPS->new($mailsettings{'SMTPSERVER'},
		Timeout => 60,
		Debug => 1,
		doSSL => 'ssl',
		Port => $mailsettings{'PORT'})) {
			system ("/bin/touch", "$errfile"); die "Could not connect to $mailsettings{'SMTPSERVER'}: $!\n";
	}
	$smtp->auth($mailsettings{'USER'}, $mailsettings{'EMAIL_PASSWORD'}) || die "Authentication failed!\n";
	&common;
}

sub send_mail_starttls {
	if (not $smtp = Net::SMTPS->new($mailsettings{'SMTPSERVER'},
		Timeout => 60,
		Debug => 1,
		Port => $mailsettings{'PORT'},
		doSSL => 'starttls',
		SSL_version=>'TLSv1')) {
			system ("/bin/touch", "$errfile"); die "Could not connect to $mailsettings{'SMTPSERVER'}: $!\n";
	}
	$smtp->auth($mailsettings{'USER'}, $mailsettings{'EMAIL_PASSWORD'}) || die "Authentication failed!\n";
	&common;
}

sub common {
	$smtp->mail($mailsettings{'FROM'} . "\n");
	$smtp->to($mailsettings{'EMAIL'});
	$smtp->cc($mailsettings{'CC'}) if $mailsettings{'CC'};
	$smtp->data();
	$smtp->datasend("To: $mailsettings{'EMAIL'}\n");
	$smtp->datasend("CC: $mailsettings{'CC'}\n") if $mailsettings{'CC'};
	$smtp->datasend("From: $mailsettings{'FROM'}\n");
	if ($ENV{NOTIFYTYPE}) {
		$smtp->datasend("Subject: $ENV{UPSNAME}: $ENV{SUBJECT}\n");
	}
	else {
		$smtp->datasend("Subject: $ARGV[0]\n");
	}
	$smtp->datasend("Date: $maildate\n");
	$smtp->datasend("MIME-Version: 1.0\n");
	$smtp->datasend("Content-type: multipart/mixed;\n\tboundary=\"_frontier_\"\n");
	$smtp->datasend("\n");
	$smtp->datasend("--_frontier_\n");
	$smtp->datasend("Content-type: text/plain\n");
	$smtp->datasend("Content-Disposition: quoted-printable\n");
	$smtp->datasend("\n$ENV{UPSNAME}: $ENV{SUBJECT}\n") if $ENV{SUBJECT};
	$smtp->datasend("\n$ARGV[0]\n") if $ARGV[0];
	$smtp->datasend("\n @upsdata\n") if @upsdata;
	$smtp->datasend("\n");
	$smtp->datasend("--_frontier_\n");
	$smtp->dataend();
	if ($mailsettings{'SMSEMAIL'}) {
		$smtp->mail($mailsettings{'FROM'} . "\n");
		$smtp->to($mailsettings{'SMSEMAIL'});
		$smtp->data();
		$smtp->datasend("To: $mailsettings{'SMSEMAIL'}\n");
		$smtp->datasend("From: $mailsettings{'FROM'}\n");
		if ($ENV{NOTIFYTYPE}) {
			$smtp->datasend("Subject: $ENV{UPSNAME}: $ENV{SUBJECT}\n");
		}
		else {
			$smtp->datasend("Subject: $ARGV[0]\n");
		}
		$smtp->datasend("Date: $maildate\n");
		$smtp->datasend("MIME-Version: 1.0\n");
		$smtp->datasend("Content-type: multipart/mixed;\n\tboundary=\"_frontier_\"\n");
		$smtp->datasend("\n");
		$smtp->datasend("--_frontier_\n");
		$smtp->datasend("Content-type: text/plain\n");
		$smtp->datasend("Content-Disposition: quoted-printable\n");
		$smtp->datasend("\n$ENV{UPSNAME}: $ENV{SUBJECT}\n\n") if $ENV{SUBJECT};
		$smtp->datasend("\n$ARGV[0]\n\n") if $ARGV[0];
		$smtp->datasend("@upstimeleft") if @upstimeleft;
		$smtp->datasend("@upsstatus") if @upsstatus;
		$smtp->datasend("@upscharge") if @upscharge;
		$smtp->datasend("\n");
		$smtp->datasend("--_frontier_\n");
		$smtp->dataend();
	}
	$smtp->quit;
	if ($mailsettings{'EMAIL'}) {
		$TO = " $mailsettings{'EMAIL'}";
	}
	if ($mailsettings{'CC'}) {
		$CC = " $mailsettings{'CC'}";
	}
	if ($mailsettings{'SMSEMAIL'}) {
		$SMS = " $mailsettings{'SMSEMAIL'}";
	}
	open FILE, ">>$log" or die $!;
	if ($ENV{NOTIFYTYPE}) {
		my $pad = '';
		for (0..13 - (length($ENV{NOTIFYTYPE}))) {
			$pad = $pad . ' ';
		}
		print FILE "$logdate  $ENV{NOTIFYTYPE}${pad}Alert sent to:$TO$CC$SMS\n";
	}
	else {
		print FILE "$logdate  APCUPSD Test  Alert sent to:$TO$CC$SMS\n";
	}
	close FILE;
}

