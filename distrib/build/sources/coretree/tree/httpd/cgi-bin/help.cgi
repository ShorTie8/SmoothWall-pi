#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use strict;
use warnings;

our (%glossary, %uisettings);
&readhash("${swroot}/main/uisettings", \%uisettings);

my ($needhelpwith, $helpPath);

my $modbase = "/var/smoothwall/mods";
my $tmp = '';
my $modname = '';
my $line = '';

# What do we need help with?
#print STDERR "Help GET:$ENV{'QUERY_STRING'}\n";

($tmp, $modname) = split("/", $ENV{'QUERY_STRING'}) if ($ENV{'QUERY_STRING'});

if ($tmp eq "logs.cgi") { $tmp = $modname; }
if ($tmp ne "mods") {
	# This is a stock help file.
	$needhelpwith = $tmp;
	$tmp = "";
	$modname = "";
	$helpPath = "";
#print STDERR "stk: helpwith=$needhelpwith tmp=$tmp name=$modname path=$helpPath\n";
}
else {
	# This is a mod's help file.
	$helpPath = "/var/smoothwall/mods/$modname";
	$needhelpwith = $ENV{'QUERY_STRING'};
	$needhelpwith =~ s=.*/==;
#print STDERR "mod: helpwith=$needhelpwith tmp=$tmp name=$modname path=$helpPath\n";
}

unless ($needhelpwith =~ /^[A-Za-z0-9\.]+$/) {
	$needhelpwith = 'index.cgi';
}
#print STDERR "final: helpwith=$needhelpwith tmp=$tmp name=$modname path=$helpPath\n";

# Prepare to display
&showhttpheaders();

&openpage($tr{'help'}, 1, '', 'help');

print "<div>";
&openbigbox();

&openbox('');

# Tricky part. We want only the language glossaries; each language could have
#   completely different glossaries, unlike UI strings. In help's case, we don't
#   overwrite English. If there's no $language glossary, there are no
#   pop-up tool tips.
# Look for the help file. If found, then read the glossaries. No sense in wasting
#   CPU cycles reading glossaries if no help file is available.
# The first help file found satisfies the request. Thus it's possible for mods to
#   completely override stock help.

if ($uisettings{'ALWAYS_ENGLISH'} ne 'off') {
	# English only. But include all mods' glossaries
	my $enGlob = "/usr/lib/smoothwall/langs/glossary.en.pl";
	$enGlob .= " $modbase/*/usr/lib/smoothwall/langs/glossary.en.pl";

	# Read the help file, if any
	while (<$helpPath/httpd/html/help/$needhelpwith.html.en>) {
		if (-f $_) {
			open (FILE, $_);
			# include all English glossaries
			# mods can override/supplement stock glossaries
			while (glob $enGlob) {
				if (-f $_) {
					require $_;
				}
			}
			last;
		}
	}
}
else {
	# Other language only. But include all mods' glossaries for that language.
	my $nonEnGlob = "/usr/lib/smoothwall/langs/glossary.$language.pl";
	$nonEnGlob .= " $modbase/*/usr/lib/smoothwall/langs/glossary.$language.pl";

	# Read the help file, if any
	while (<$helpPath/httpd/html/help/$needhelpwith.html.$language>) {
		if (-f $_) {
			open (FILE, $_);
			# include all $language glossaries
			# mods can override/supplement stock glossaries
			while (glob $nonEnGlob) {
				if (-f $_) {
					require $_;
				}
			}
			last;
		}
	}
}
require "/usr/lib/smoothwall/langs/glossary.base.pl";

# Read the help file.
while ( <FILE> ){
	$line =~s/\n/ /g;
	$line .= $_;
}
close (FILE);

print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td class='helpheader'>
		<a href="javascript:window.close();"><img src="/ui/img/help.footer.png" alt="Smoothwall Express Online Help - click to close window"></a>
	</td>
</tr>
<tr>
	<td style='text-align: justify; font-size: 11px;'>
END
;

foreach my $term ( keys %glossary ){
	$line =~s/([\W])($term)([^\w:])/$1\01$2\02$term\03$3/ig;
	$glossary{$term} =~ s/(['\\"])/\\$1/g;
}

$line =~ s/\01([^\02]*)\02([^\03]*)\03/<span style='color: #008b00;' onMouseOver="return Tip('$glossary{$2}');" onmouseout="UnTip();">$1<\/span>/ig;
print $line;

print <<END
	</td>
</tr>
<tr>
	<td class='helpfooter'>
		<a href="javascript:window.close();"><img style='border-style: none;' alt="Close this window" src="/ui/img/help.footer.png"></a>
	</td>
</tr>
</table>
END
;

&closebox();

&closebigbox();
print "</div>";
&closepage('blank');

