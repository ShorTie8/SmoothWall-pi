# SmoothWall Express "Header" Module
#
# This code is distributed under the terms of the GPL
#
# (c) 2004-2005 SmoothWall Ltd

package header;
require Exporter;
use Data::Dumper;
@ISA = qw(Exporter);

# define the Exportlists.

our @_validation_items;

@EXPORT       = qw();
@EXPORT_OK    = qw( $language $version $displayVersion $webuirevision
                    $viewsize @menu $swroot $thisscript showhttpheaders
                    showmenu showsection openpage closepage openbigbox
                    closebigbox openbox closebox alertbox pageinfo readvalue
                    writevalue writehash readhash getcgihash log pipeopen age
                    validip validmask validipormask validipandmask validipandmasks validport validarchivename
                    validportrange validmac validhostname validcomment UTC2LocalString
                    basename dirname connectedstate %tr @_validation_items getsystemid
                    outputfile getLinkSpeed requireConditional %filters %optionText);
%EXPORT_TAGS  = (
      standard   => [@EXPORT_OK],
      );


# Conditional require

sub requireConditional
{
	my ($incFile) = @_;
	if (-f $incFile) {
		require $incFile;
		return 1;
	}
	else {
		return 0;
	}
}


$| = 1; # line buffering

# some constant defaults.

$swroot = '/var/smoothwall';
if (defined $ENV{'SCRIPT_NAME'}) {
	$thisscript = $ENV{'SCRIPT_NAME'};
	$thisscript =~ s/^\///;
	$thisscript =~ s/^cgi-bin\///;
}
else {
	$thisscript = "";
}

# Work out some various details from the various system files.
# such as fixes number etc.

my %productdata;
&readhash( "/var/smoothwall/main/productdata", \%productdata );

# This is used for some filenames, I think; it must have this form.
$version = "$productdata{'VERSION'}-$productdata{'REVISION'}-$productdata{'ARCH'}";

# This is used to display the version in the UI and in smoothinfo.
if (! -z "${swroot}/patches/installed") {
	open (INSTALLED,"<${swroot}/patches/installed") || die "Unable to open $!";
	my @installed = (<INSTALLED>);
	close (INSTALLED);

	my $patch = pop (@installed);
	my @update = split (/\|/, $patch);
	my $updatenumber = $update[1];
	$updatenumber =~ s/-i586//;
	$updatenumber =~ s/-x86_64//;

	$displayVersion = "$productdata{'PRODUCT'} $productdata{'VERSION'}$productdata{'EXTRA'}";
	$displayVersion .= "-$productdata{'REVISION'}-$productdata{'ARCH'}-$updatenumber";
}
else {
	$displayVersion = "$productdata{'PRODUCT'} $productdata{'VERSION'}$productdata{'EXTRA'}";
	$displayVersion .= "-$productdata{'REVISION'}-$productdata{'ARCH'}";
}

$webuirevision = $productdata{'UI_VERSION'};
$viewsize = 200;

# some system wide (yuck) global variables.  not pretty, but make things easier.

my @menu;
my $span = 0;

use Net::Domain qw(hostname hostfqdn hostdomain);
my $hostname = hostfqdn();


# customised settings (such as languages)

&readhash("${swroot}/main/settings", \%settings);
$uisettings{'ALWAYS_ENGLISH'} = 'on';
&readhash("${swroot}/main/uisettings", \%uisettings);
my $languages = $ENV{HTTP_ACCEPT_LANGUAGE} || 'en';
my ($language, @junk) = split(/,/, $languages);
$language =~ tr/A-Z/a-z/;

# Pull in the stock en.pl and all the mods' en.pl files.
require "/usr/lib/smoothwall/langs/en.pl";
while (</var/smoothwall/mods/*/usr/lib/smoothwall/langs/en.pl>) {
	requireConditional $_;
}

if (${language} ne "en" && $uisettings{'ALWAYS_ENGLISH'} eq 'off') {
	foreach $key (sort keys %basetr) {
		$basetr{$key} = "[$basetr{$key}]"
	}
	requireConditional "/usr/lib/smoothwall/langs/${language}.pl";
	while (</var/smoothwall/mods/*/usr/lib/smoothwall/langs/${language}.pl>) {
		requireConditional $_;
	}
}
require "/usr/lib/smoothwall/langs/base.pl";

# Pull in the alertboxes.en.pl files.
# First, pull in the EN alertbox text.
if (not $thisscript =~ /^mods\//) {
	# Pull in the stock en.pl and each mod's en.pl file.
	# Only need the *one* text.
	# The last mod that provids one wins.
	require "/usr/lib/smoothwall/langs/alertboxes.en.pl";
	$abouttext{$thisscript} = $baseabouttext{$thisscript};
	undef %baseabouttext;

	while (</var/smoothwall/mods/*/usr/lib/smoothwall/langs/alertboxes.en.pl>) {
		requireConditional $_;
		if (defined $baseabouttext{$thisscript}) {
			$abouttext{$thisscript} = $baseabouttext{$thisscript};
		}
		undef %baseabouttext;
	}
}
else {
	# Pull in the mod's alertboxes.en.pl.
	my $mod = $thisscript;
	$mod =~ s/mods\///;
	$mod =~ s/\/.*//;
	$_ = "/var/smoothwall/mods/$mod/usr/lib/smoothwall/langs/alertboxes.en.pl";
	if (requireConditional $_) {
		if (defined $baseabouttext{$thisscript}) {
			$abouttext{$thisscript} = $baseabouttext{$thisscript};
		}
	}
	undef %baseabouttext;
}

# Pull in the alertboxes.'lang'.pl files if needed. These will override the
# EN texts.
if (${language} ne "en" && $uisettings{'ALWAYS_ENGLISH'} eq 'off') {
	foreach $key (sort keys %abouttext) {
		$abouttext{$key} = "[$abouttext{$key}]"
	}
	# First, pull in the 'lang' alertbox text.
	if (not $thisscript =~ /^mods\//) {
		# Pull in the stock alertbox.'lang'.pl and each mod's alertbox.'lang'.pl file.
		# Only need the *one* text.
		# The last mod that provides one wins. If none, stock wins.
		requireConditional "/usr/lib/smoothwall/langs/alertboxes.$language.pl";
		if (defined $baseabouttext{$thisscript}) {
			$abouttext{$thisscript} = $baseabouttext{$thisscript};
		}
		undef %baseabouttext;
		while (</var/smoothwall/mods/*/usr/lib/smoothwall/langs/alertboxes.$language.pl>) {
			requireConditional $_;
			if (defined $baseabouttext{$thisscript}) {
				$abouttext{$thisscript} = $baseabouttext{$thisscript};
			}
			undef %baseabouttext;
		}
	}
	else {
		# Pull in the mod's alertboxes.'lang'.pl.
		my $mod = $thisscript;
		$mod =~ s/mods\///;
		$mod =~ s/\/.*//;
		$_ = "/var/smoothwall/mods/$mod/usr/lib/smoothwall/langs/alertboxes.$language.pl";
		if (requireConditional $_) {
			if (defined $baseabouttext{$thisscript}) {
				$abouttext{$thisscript} = $baseabouttext{$thisscript};
			}
		}
		undef %baseabouttext;
	}
}


# Display the page HTTP header

sub showhttpheaders
{
	print "Pragma: no-cache\n";
	print "Cache-control: no-cache\n";
	print "Connection: close\n";
	print "Content-type: text/html\n\n";
}

# Show the top section menu, this has the side effect of populating
# the @menu variable (which is ordered accordingly) with the pages
# or subsections for the section we are looking for.


sub showmenu
{
	$scriptname = $_[0];

	# load the list of sections from the relevant locations.
	my @rawsections = <"/var/smoothwall/mods/*/usr/lib/smoothwall/menu/*" "/usr/lib/smoothwall/menu/*">;

	# Strip the path off to get the section name; use that as a hash key to store unique sections
	foreach my $rawsection (@rawsections) {
		my $idx = $rawsection;
		chomp $idx;
		$idx =~ s=.*/==;
		$sections{$idx} = 1;
	}

	my $first = "";

	my $menu_html;
	my @clear_sections;
	my $file;

	# For each unique section
	foreach my $sectionkey ( sort(keys(%sections)) ) {
		my %pages;
		my @tempmenu;
		my $section = "no";

		# Get all .list files in them
		my @lists = </usr/lib/smoothwall/menu/$sectionkey/*.list>;
		@lists = (@lists, </var/smoothwall/mods/*/usr/lib/smoothwall/menu/$sectionkey/*.list>);

		# Store the full paths by .list filename in assoc. array.
		foreach my $list (@lists) {
			my $idx = basename($list);
			$pages{$idx} = dirname($list);
		}
         
		# Traverse through the UI pages (*.list)
		foreach my $page ( sort(keys(%pages))) {
			# Set $menuprefix and $file (used to be set differently in SWE3.0)
			my $menuprefix = dirname($pages{$page});
			my $urlPath = $menuprefix;
			if ( $urlPath =~ /^\/var\/smoothwall\/mods/ ) {
				$urlPath =~ s=/var/smoothwall/mods/==;
				$urlPath =~ s=/.*==;
				$urlPath = "/mods/".$urlPath."/cgi-bin/";
			}
			else {
				$urlPath = "/cgi-bin/";
			}
			$file = basename($pages{$page});
			open DETAIL, "<$menuprefix/$file/$page" or next;
			my $listLine = <DETAIL>;
			close DETAIL;
			chomp $listLine;

			# next if the file is empty or conains a bare ':', or contains '#erase stock'
			next if ($listLine eq "" or $listLine eq ":" or $listLine eq "#erase stock");
			my ( $title, $link ) = split(/:/, $listLine);
			my ( $menu, $pos ) = ( $file =~ /(\d{2})(\d{2}).*/ );
			my $active = "";
			#my ( $link2 ) = ( $link =~/([^\/]*)$/ );
			if ( $urlPath.$link eq $ENV{'SCRIPT_NAME'} ) {
				$section = "yes";
				$active = "true";
				$helpPath = $urlPath;
				if ($helpPath =~ m=.*/mods/.*=) {
					#$helpPath =~ s=/cgi-bin/==;
					$helpPath = "";
				}
				else {
					$helpPath = "";
				}
			}
			push @tempmenu, { 'title' => $title, 'href' => $link, 'active' => $active, 'urlPath' => $urlPath };
		}
		if ( scalar(@tempmenu) > 0 ) {
			my ( $section_title ) = ( $file =~/\d{4}_(.*)/ );

			if ( $section eq "yes" ) {
				@menu = @tempmenu;
				$menu_html .= "<td>$first<a class='activemenu' href='$menu[ 0 ]->{'urlPath'}$menu[ 0 ]->{'href'}'>$section_title</a></td>";
			}
			else {
				unless ( defined $uisettings{'MENU'} and $uisettings{'MENU'} eq "off") {
					$menu_html .= qq |
	<td>
		<div class='menushaddow' id='${section_title}shadow'>
|;
					$menu_html .= &showhovermenu( @tempmenu );
					$menu_html .= qq |
		</div>
|;
					$menu_html .= qq |
		<div class='menu' id='$section_title'
			onMouseOver="menu_show('$section_title')"
			onMouseOut="menu_clear();">
|;
					$menu_html .= &showhovermenu( @tempmenu );
					$menu_html .= qq |
		</div>
	</td>
	<td onMouseOver="menu_show('$section_title');"
		onMouseOut="menu_clear();">
		$first<a class='menu' href="$tempmenu[ 0 ]->{'urlPath'}$tempmenu[ 0 ]->{'href'}">$section_title</a>
	</td>
|;
				}
				else {
					$menu_html .= qq |
	<td>
		$first<a class='menu' href="$tempmenu[ 0 ]->{'urlPath'}$tempmenu[ 0 ]->{'href'}">$section_title</a>
	</td>
|;
				}
				push @clear_sections, $section_title;
			}
			# Set the displayed separator between items
			$first = " | ";
		}
	}
	print <<END
<tr>
	<td class='mainmenu'>
		<script TYPE="text/javascript">
		function menu_clear( me )
		{
END
;

	foreach my $option ( @clear_sections ){
		print "\t\t\tif( me != '$option') document.getElementById('$option').style.display = 'none';\n";
		print "\t\t\tif( me != '$option') document.getElementById('${option}shadow').style.display = 'none';\n";
	}
	print <<END
		}
		function menu_show( what ){
			menu_clear();
			document.getElementById(what).style.display = 'block';
			document.getElementById( what+'shadow' ).style.display = 'block';
		}
		</script>
<table style='float: right;'>
<tr>
END
;

	print $menu_html;

	print <<END
	<td>
		<p style="margin:2px 2px 4px 1em; vertical-align:top">
		<a style='color:#ff8866' href="javascript:displayHelp('$helpPath$thisscript');" title="This will popup a new window with the requested help file">Help <img src="/ui/img/help.gif" alt="" style='vertical-align:middle'></a></p>
	</td>
</tr></table></td>
</tr></table>
	</td>
	<td style="background-image:url(/ui/img/frame-concrete/wrs.png); max-width:8px; width:8px;
		min-width:8px; background-repeat:repeat-y"></td>
</tr>
<tr>
	<td style="background-image:url(/ui/img/frame-concrete/wbl.png); max-height:8px; height:8px;
		min-height:8px; max-width:8px; min-width:8px; background-repeat:none"></td>
	<td style="background-image:url(/ui/img/frame-concrete/wbs.png); max-height:8px; height:8px;
		min-height:8px; background-repeat:repeat-x"></td>
	<td style="background-image:url(/ui/img/frame-concrete/wbr.png); max-height:8px; height:8px;
		min-height:8px; max-width:8px; width:8px; min-width:8px; background-repeat:none"></td>
</tr>
</table>

<!-- Create the main content -->

<table class='frame' cellpadding='0' cellspacing='0' style='margin:.5em 0em .5em 2em; text-align:left;'>
<tr style="margin:0">
	<td style="background-image:url(/ui/img/top-left.png); max-height:4px; height:4px;
		min-height:4px; max-width:6px; min-width:6px; background-repeat:none"></td>
	<td style="background-image:url(/ui/img/top.png); max-height:4px; height:4px;
		min-height:4px; background-repeat:repeat-x"></td>
	<td style="background-image:url(/ui/img/top-right.png); max-height:4px; height:4px;
		min-height:4px; max-width:4px; width:4px; min-width:4px; background-repeat:none"></td>
</tr>
<tr style="margin:0">
	<td style="background-image:url(/ui/img/left.png); max-width:6px; width:6px;
		min-width:6px; background-repeat:repeat-y"></td>
	<td>
		<table class='main' cellpadding='0' cellspacing='0' style='padding:1em'>

<tr>
	<td>
END
;

	showsection( @menu );
	return;
}

sub showhovermenu
{
	my @tempmenu = @_;
	my $html;
	foreach my $item ( @tempmenu ){
		my $width = 8 + (8 * length( $tr{ $item->{'title'} } ));
		if ( defined $item->{'active'} and $item->{'active'} eq "true" ){
			$html .= "<a class='menushade' href='$item->{'urlPath'}$item->{'href'}'>$tr{$item->{'title'}}</a><br />";
		}
		else {
			$html .= "<a class='menushade' href='$item->{'urlPath'}$item->{'href'}'>$tr{$item->{'title'}}</a><br />";
		}
		$span++;
		$remaining -= $width;
	}
	return $html;
}

sub showsection
{
	my @menu = @_;
	print <<END
<table class='mainmenu'>
<tr>
END
;

	my $remaining = 795;

	$span = 0;
   
	foreach my $item ( @menu ){
		my $width = 8 + (8 * length( $tr{ $item->{'title'} } ));
		if ( defined $item->{'active'} and $item->{'active'} eq "true" ){
			print "<td class='activetab' style='width: ".( $width + 16 )."px;'><a href='$item->{'urlPath'}$item->{'href'}'>$tr{$item->{'title'}}</a> </td>";
		}
		else {
			print "<td  class='inactivetab' style='width: ${width}px;'><a href='$item->{'urlPath'}$item->{'href'}'>$tr{$item->{'title'}}</a> </td>";
		}
		$span++;
		$remaining -= $width;
	}
	$span++;

	print <<END
	<td style='width:${remaining}px' class='endtab'>&nbsp;</td>
</tr>
<tr>
	<td class='mainbody' colspan='$span'>
END
;
}


sub openpage
{
	($title,$menu,$extrahead,$thissection,$overrideStyle,$unused) = @_;

	if ($menu == 1) {
		$colspan = 2;
	}
	else {
		$colspan = 1;
	}

	my %netsettings;
	&readhash("${swroot}/ethernet/settings", \%netsettings);
	my ($redip, $orangeip, $greenip, $purpleip, $dns1, $dns2) = ('','','','','','');
	my $startcell = '<td style="font-size:8pt; padding:0 .4em; border:none; background-color:';

	my $displayName = $hostname;
	if (length($hostname) > 24) {
		$displayName = hostname();
	}
	my $system = $startcell.'none"><span style="color:black; font-weight:bold;">'.$displayName.'</span></td>';

	open (FILE, "${swroot}/red/local-ipaddress");
	while (<FILE>) {
		chomp;
		$redip = $startcell.'#FF9999"><span style="color:black">Red IP:';
		$redip .= ' <span style="float:right; font-weight:bold;">'.$_.'</span></span></td>';
	}
	close (FILE);

	if ($netsettings{'ORANGE_ADDRESS'}) {
		$orangeip = $startcell.'#FFAA77"><span style="color:black">Orange IP:';
		$orangeip .= ' <span style="float:right; font-weight:bold;">';
		$orangeip .= $netsettings{'ORANGE_ADDRESS'}.'</span></span></td>';
	}
	else {
		$orangeip = $startcell.'#FFAA77"><span style="color:black">Orange IP:';
		$orangeip .= ' <span style="float:right; font-weight:bold;">Not Available</span></span></td>';
	}
   
	if ($netsettings{'PURPLE_ADDRESS'}) {
		$purpleip = $startcell.'#DDAAFF"><span style="color:black">Purple IP:';
		$purpleip .= ' <span style="float:right; font-weight:bold;">';
		$purpleip .= $netsettings{'PURPLE_ADDRESS'}.'</span></span></td>';
	}
	else {
		$purpleip = $startcell.'#DDAAFF"><span style="color:black">Purple IP:';
		$purpleip .= ' <span style="float:right; font-weight:bold;">Not Available</span></span></td>';
	}

	if ($netsettings{'GREEN_ADDRESS'}) {
		$greenip = $startcell.'#99FF99"><span style="color:black">Green IP:';
		$greenip .= ' <span style="float:right; font-weight:bold;">';
		$greenip .= $netsettings{'GREEN_ADDRESS'}.'</span></span></td>';
	}

	open (FILE, "${swroot}/red/dns1");
	while (<FILE>) {
		chomp;
		$dns1 = $startcell.'#F0E68C"><span style="color:black">DNS 1:';
		$dns1 .= ' <span style="float:right; font-weight:bold;">'.$_.'</span></span></td>';
	}
	close (FILE);

	open (FILE, "${swroot}/red/dns2");
	while (<FILE>) {
		chomp;
		$dns2 = $startcell.'#F0E68C"><span style="color:black">DNS 2:';
		$dns2 .= ' <span style="float:right; font-weight:bold;">'.$_.'</span></span></td>';
	}
	close (FILE);

	my $locks = scalar(glob("/var/run/ppp-*.pid"));
	my $theconnstate;
	if ( -e "${swroot}/red/active" ) {
		$theconnstate = $startcell.'#99FF99"><span style="color:black">Red Status:';
		$theconnstate .= '<span style="float:right; font-weight:bold;">Connected</span></span></td>';
	}
	elsif ($locks) {
		$theconnstate = $startcell.'#FFD700"><span style="color:black">Red Status:';
		$theconnstate .= '<span style="float:right; font-weight:bold;">Connecting</span></span></td>';
	}
	else {
		$theconnstate = $startcell.'#C0C0C0"><span style="color:black">Red Status:';
		$theconnstate .= '<span style="float:right; font-weight:bold;">Idle</span></span></td>';
	}

	print <<END
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
	$extrahead
	<title>($hostname) $title - Smoothwall Express</title>
	<script type="text/javascript" src='/ui/js/script.js'></script>
	<link href='/ui/css/style.css' rel='stylesheet' type='text/css'>
	<script type="text/javascript">
		function setVisibility(id) {
		if(document.getElementById('button1').value=='Hide IP') {
			document.getElementById('button1').value = 'Show IP';
			document.getElementById('button1').style.display = 'inline';
			document.getElementById(id).style.display = 'none';
		}
		else {
			document.getElementById('button1').value = 'Hide IP';
			document.getElementById('button1').style.display = 'none';
			document.getElementById(id).style.display = 'inline';
		}
	}
	</script>
END
;

	# Override the default style, if specified
	if (defined($overrideStyle)) {
		print <<END
	<link href='/ui/css/$overrideStyle.css' rel='stylesheet' type='text/css'>
END
;
	}

	print <<END
</head>
END
;

	if ( $thissection ne "help" ) {
		# $cellwidth = $pagewidth / 2;
		print <<END
<body>

<!-- Create the top box -->

<table class='frame' cellpadding='0' cellspacing='0' style='margin:1em 0em .5em 2em; text-align:left;'>
<tr style="margin:0">
	<td style="background-image:url(/ui/img/frame-concrete/wtl.png); max-height:8px; height:8px;
		min-height:8px; max-width:8px; min-width:8px; background-repeat:none"></td>
	<td style="background-image:url(/ui/img/frame-concrete/wts.png); max-height:8px; height:8px;
		min-height:8px; background-repeat:repeat-x"></td>
	<td style="background-image:url(/ui/img/frame-concrete/wtr.png); max-height:8px; height:8px;
		min-height:8px; max-width:8px; width:8px; min-width:8px; background-repeat:none"></td>
</tr>
<tr style="margin:0">
	<td style="background-image:url(/ui/img/frame-concrete/wls.png); max-width:8px; width:8px;
		min-width:8px; background-repeat:repeat-y"></td>
	<td>
		<table class='main' cellpadding='0' cellspacing='0'>
		<tr>
			<td class='logo' rowspan='2'></td>
			<td class='header'>

				<table border='0' style="float:right" title="Click to show">
				<tr>
					<td style="font-size:10pt"><input id='button1' type=button name=type value='Show IP'
						onclick="setVisibility('iptable');"></td>
					<td style="width:50px"></td> <!-- Dont Use (Spacing) -->
				</tr>
				</table>

				<div id='iptable' title='Click to Hide' style='display:none'
					onclick="setVisibility('iptable');">
				<table width="70%" border="0" cellpadding="0" cellspacing="0"
					style="text-align:left; margin:0 0 0 16em;">
				<tr>
					$system
					$greenip
					$orangeip
					$dns1
					<td style="width:50px"></td> <!-- Dont Use (Spacing) -->
				</tr>
				<tr>
					$theconnstate
					$redip
					$purpleip
					$dns2
					<td></td> <!-- Dont Use (Spacing) -->
				</tr>
				</table>
				</div></td>
END
;

		&showmenu($thissection);
	}
	else {
		print <<END
<body onLoad="window.focus()" style="background:white">
END
;
	}
}


sub closepage
{
	$thissection = $_[0];
	$sflogoimg = "/ui/assets/3.5/img/sflogo.png";

	if ( not defined $thissection or $thissection ne "blank" ) {
		print <<END
			</td>
		</tr>
			<!-- End of the Main Body -->
		</table>
	</td>
</tr></table>
	</td>
	<td style="background-image:url(/ui/img/right.png); max-width:4px; width:4px;
		min-width:4px; background-repeat:repeat-y"></td>
</tr>
<tr>
	<td style="background-image:url(/ui/img/bottom-left.png); max-height:6px; height:6px;
		min-height:6px; max-width:6px; min-width:6px; background-repeat:none"></td>
	<td style="background-image:url(/ui/img/bottom.png); max-height:6px; height:6px;
		min-height:6px; background-repeat:repeat-x"></td>
	<td style="background-image:url(/ui/img/bottom-right.png); max-height:6px; height:6px;
		min-height:6px; max-width:4px; width:4px; min-width:4px; background-repeat:none"></td>
</tr>
</table>

<!-- Create the footer -->

<table class='frame' cellpadding='0' cellspacing='0' style='text-align:left; margin:.5em 0em 1em 2em;'>
<tr style="margin:0">
	<td style="background-image:url(/ui/img/frame-concrete/wtl.png); max-height:8px; height:8px;
		min-height:8px; max-width:8px; min-width:8px; background-repeat:none"></td>
	<td style="background-image:url(/ui/img/frame-concrete/wts.png); max-height:8px; height:8px;
		min-height:8px; background-repeat:repeat-x"></td>
	<td style="background-image:url(/ui/img/frame-concrete/wtr.png); max-height:8px; height:8px;
		min-height:8px; max-width:8px; width:8px; min-width:8px; background-repeat:none"></td>
</tr>
<tr style="margin:0">
	<td style="background-image:url(/ui/img/frame-concrete/wls.png); max-width:8px; width:8px;
		min-width:8px; background-repeat:repeat-y"></td>
	<td>
		<table class='main' cellpadding='0' cellspacing='0'>

<tr>
	<td class='footer' colspan='2' style='width:100%'>
		<div style="width:37%; text-align:left; margin:2px; display:inline-block; float:left">
		<strong>Smoothwall $displayVersion</strong><br/>
		Smoothwall&trade; is a trademark of <a href='http://www.smoothwall.net/'>Smoothwall Limited</a>.</div>
		<p id='currentTime' style='margin:.1em 0 0 0; width:25%;
			text-align:center; display:inline-block'></p>
		<div style="width:37%; text-align:right; margin:2px; float:right">
			&copy; 2000 - 2018 <a href='http://smoothwall.org/about/team/'>The Smoothwall Team</a><br/>
			<a href='/cgi-bin/register.cgi'>$tr{'credits'}</a> - Portions &copy; <a href='http://www.smoothwall.org/download/sources/'>original authors</a></div></td>
</tr>
</table>

<script type='text/javascript' src='/ui/js/monitor.js'></script>
<script type='text/javascript'>

	var timeMonitorObj = new Object();

	function doTime () {
		simpleMonitor(timeMonitorObj, '/cgi-bin/time-clock.cgi', displayTime);
	}

	function displayTime(dateTime) {
		document.getElementById('currentTime').innerHTML = 'Firewall Time<br /><span style="color:#505050; font-size:10pt; font-weight:bold;">'+ dateTime +'<' + '/span>';
	}
	var timeTimer = setInterval (doTime, 1000);
</script>

	</td>
	<td style="background-image:url(/ui/img/frame-concrete/wrs.png); max-width:8px; width:8px;
		min-width:8px; background-repeat:repeat-y"></td>
</tr>
<tr>
	<td style="background-image:url(/ui/img/frame-concrete/wbl.png); max-height:8px; height:8px;
		min-height:8px; max-width:8px; min-width:8px; background-repeat:none"></td>
	<td style="background-image:url(/ui/img/frame-concrete/wbs.png); max-height:8px; height:8px;
		min-height:8px; background-repeat:repeat-x"></td>
	<td style="background-image:url(/ui/img/frame-concrete/wbr.png); max-height:8px; height:8px;
		min-height:8px; max-width:8px; width:8px; min-width:8px; background-repeat:none"></td>
</tr>
</table>

END
;

	}

	if ( not defined $thissection or $thissection ne "update" ) {
		print <<END
	<script TYPE="text/javascript" SRC='/ui/js/wz_tooltip.js'></script>
	<script TYPE="text/javascript">
END
;

		foreach my $item ( @_validation_items ) {
			print "$item;\n";
		}

		print <<END
	</script>
</body>
</html>
END
;
	}
}

sub openbigbox
{
}

sub closebigbox
{
}

sub openbox
{
	my ( $caption ) = @_;

	print <<END
<br />
<table class='box'>
<tr>
	<td>
END
;

	if ($caption) {
		print "<span class='caption'>$caption</span><br />\n";
	}
}

sub closebox
{
	print <<END
	</td>
</tr>
</table>
<br />
END
;
}

sub alertbox
{
	my $thiserror = $_[0];
	my $additional = $_[1];
	my $thisinfo = $_[2];

	if ( $thiserror eq 'add' && $additional eq 'add' && $abouttext{$thisscript . "-additional"} ne '' ) {
		&pageinfo( $alertbox{"textadd"}, $abouttext{$thisscript . "-additional"});
	}
	elsif ( $thiserror eq 'add' && $additional eq 'add' && $abouttext{$thisscript . "-additional"} eq '' ) {
		# deliberately do nothing
	}
	else {
		&pageinfo( $alertbox{"textok"}, $abouttext{$thisscript});
	}

	if ( $thiserror ne '' && $additional eq '' ) {
		&pageinfo( "error", $thiserror);
	}
	if ($thisinfo ne '') {
		&pageinfo( "info", $thisinfo);
	}
}

sub pageinfo
{
	my $thisalerttype = $_[0];
	my $thisboxmessage = $_[1];

	print <<END
<br />
END
;

	if ( $thisalerttype eq "error" ) {
		print "<table class='warning'>";
		print "<tr>";
		print "	<td class='warningimg'><img src='/ui/img/x-icon.png' alt='$tr{'error'}'></td><td class='warning'><strong>$tr{'error'}</strong>$thisboxmessage</td>";
	}
	elsif ( $thisalerttype eq "info" ) {
		print "<table class='info'>";
		print "<tr>";
		print "	<td class='warningimg'><img src='/ui/img/check-icon.png' alt='$tr{'error'}'></td><td class='warning'><strong>$tr{'error'}</strong>$thisboxmessage</td>";
	}
	else {
		print "<table class='note'>";
		print "<tr>";
		print "	<td class='note'>$thisboxmessage</td>";
	}


print <<END
</tr>
</table>
END
;
}

sub readvalue
{
	my ( $filename, $value ) = @_;

	unless ( open(FILE, $filename) ) {
		return undef;
	}

	while (<FILE>) {
		chomp;
		$value = $_;
	}
	close FILE;
	return $value;
}

sub writevalue
{
	my ( $filename, $value ) = @_;

	unless ( open( FILE, ">$filename" ) ) {
		return undef;
	}
	print FILE "$value\n";
	close FILE;
}

sub writehash
{
	my $filename = $_[0];
	my $hash = $_[1];
   
	# write cgi vars to the file.
	open(FILE, ">${filename}") or die "Unable to write file $filename";
	flock FILE, 2;
	foreach $var (keys %$hash) {
		$val = $hash->{$var};
		if ($val =~ / / || $val =~ /\n/) {
			$val = "\'$val\'";
		}
		if (!($var =~ /^ACTION/)) {
			print FILE "${var}=${val}\n";
		}
	}
	close FILE;
}

sub readhash
{
	my $filename = $_[0];
	my $hash = $_[1];
	my ($var, $val);

	open(FILE, $filename) or die "Unable to read file $filename";
   
	while (<FILE>) {
		chomp;
		next if ($_ =~ /^\s*#/);
		next if ($_ eq "");
		($var, $val) = split /=/, $_, 2;
		if ($var) {
			$val =~ s/^\'//g if ($val);
			$val =~ s/\'$//g if ($val);
			$hash->{$var} = $val;
		}
	}
	close FILE;
}

sub getcgihash
{
	my $hash = $_[0];
	my $buffer = '';
	my $length = $ENV{'CONTENT_LENGTH'};
	my ($name, $value);
	my ($pair, @pairs, $read);
	my %hash;
	my $boundary;
	my %remotesettings;
	my %main;
	my %netsettings;
	my $redip = '0.0.0.0';
	my $referer;
	my $shorthostname;
	my @hostnameelements;
   
	if ((!($ENV{'REQUEST_METHOD'})) or $ENV{'REQUEST_METHOD'} ne 'POST') {
		return;
	}

	$ENV{'HTTP_REFERER'} =~ m/^(http|https)\:\/\/(.*?)[\:|\/]/;
	$referer = $2;

	&readhash("${swroot}/remote/settings", \%remotesettings);
	&readhash("${swroot}/main/settings", \%main);
	&readhash("${swroot}/ethernet/settings", \%netsettings);

	@hostnameelements = split(/\./, $main{'HOSTNAME'});
	$shorthostname = $hostnameelements[0];

	if (open(FILE, "${swroot}/red/local-ipaddress")) {
		$redip = <FILE>; chomp $redip;
		close(FILE);
	}

	if ($remotesettings{'ENABLE_SECURE_ADMIN'} eq 'on') {
		unless ($referer eq $main{'HOSTNAME'}
		   || $referer eq $shorthostname
		   || $referer eq $netsettings{'GREEN_ADDRESS'}
		   || $referer eq $redip) {
			&log("Referral $ENV{'HTTP_REFERER'} is not a Smoothwall page.");
			return;
		}
	}
   
	$read = 0;
	$buffer = "";
	while($read < $length) {
		$read = $read + (read(STDIN, $buf, 1024) or die "Could not read buffer:$read: $@");
		$buffer .= $buf;
	}
	unless($read == $length) {
		die "Could not read buffer: $!";
	}

	if($ENV{'CONTENT_TYPE'} =~ m/multipart\/form-data; boundary=(.*)/) {
		$boundary = $1;
		chomp $boundary;
		$boundary =~ s/\+/ /g;
		foreach (split(/$boundary/,$buffer)) {
			s!--$!!so;
			if(m/Content-Disposition: form-data; name="(.*?)"/is) {
				$name = $1;
			}
			if(m/Content-Disposition: form-data; name="$name".*?\015\012\015\012(.*)$/is) {
				$value = $1;
				$value =~ s!\015\012$!!so;
				$hash->{$name} = $value;
			}
			else {
				next;
			}
		}
	}
	else {
		@pairs = split(/&/, $buffer);

		foreach $pair (@pairs) {
			$pair =~ s/\+/ /g;
			($name, $value) = split(/=/, $pair);
			next unless $name; # fields MUST BE named!
			$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack('C', hex($1))/eg;
			$value =~s/[^\w\013\n!@#\$%\^\*()_\-\+=\{\}\[\]\\|;:\'\"<,>\.?\/`~\& ]//g;
			$hash->{$name} = $value;
		}
	}
	return %hash;
}

sub log
{
	system('/usr/bin/logger', '-t', 'smoothwall', $_[0]);
}

sub pipeopen
{
	my $ret;
   
	open(PIPE, '-|') || exec(@_) or die "Couldn't run @_";
	while (<PIPE>) { $ret .= $_; }
	close (PIPE);

	return $ret;
}   

sub age
{
	my ($dev, $ino, $mode, $nlink, $uid, $gid, $rdev, $size,
		$atime, $mtime, $ctime, $blksize, $blocks) = stat $_[0];
	my $now = time;

	my $totalsecs = $now - $mtime;
	my $days = int($totalsecs / 86400);
	my $totalhours = int($totalsecs / 3600);
	my $hours = $totalhours % 24;
	my $totalmins = int($totalsecs / 60);
	my $mins = $totalmins % 60;
	my $secs = $totalsecs % 60;

	return "${days}d ${hours}h ${mins}m ${secs}s";
}

sub validip
{
	my $ip = $_[0];

	if (!($ip =~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/)) {
		return 0;
	}
	else {
		@octets = ($1, $2, $3, $4);
		foreach $_ (@octets) {
			if (/^0./) {
				return 0;
			}
			if ($_ < 0 || $_ > 255) {
				return 0;
			}
		}
		return 1;
	}
}

sub validmask
{
	my $mask = $_[0];

	# secord part an ip?
	return 1 if (&validip($mask));

	# second part a number?
	return 0 if (/^0/);

	return 0 if (!($mask =~ /^\d+$/));
	return 1 if ($mask >= 0 && $mask <= 32);

	return 0;
}

sub validipormask
{
	my $ipormask = $_[0];

	# see if it is a IP only.
	return 1 if (&validip($ipormask));

	# split it into number and mask.
	return 0 if (!($ipormask =~ /^(.*?)\/(.*?)$/));

	$ip = $1;
	$mask = $2;

	# first part not a ip?
	return 0 if (!(&validip($ip)));

	return &validmask($mask);
}

sub validipandmasks
{
	my @ipandmasks = split(/:/, $_[0]);
	
	# Assume all are OK.
	my $combinedRetVal = 1;

	# split it into individual ip/masks and validate each.
	foreach $ipandmask (@ipandmasks) {
		# If invalid, set to zero (not all valid).
		$combinedRetVal = 0 if !(&validipandmask($ipandmask));
	}

	return $combinedRetVal;

}

sub validipandmask
{
	my $ipandmask = $_[0];

	# split it into number and mask.
	return 0 if (!($ipandmask =~ /^(.*?)\/(.*?)$/));

	$ip = $1;
	$mask = $2;

	# first part not a ip?
	return 0 if (!(&validip($ip)));

	return &validmask($mask);
}

sub validport
{
	$_ = $_[0];

	return 0 if (!/^\d+$/);
	return 0 if (/^0./);
	return 1 if ($_ >= 1 && $_ <= 65535);

	return 0;
}

sub validportrange
{
	my $ports = $_[0];
	my $left; my $right;

	return 1 if (&validport($ports));
	if ($ports =~ /:/) {
		$left = $`;
		$right = $';
		if (&validport($left) && &validport($right)) {
			return 1 if ($right > $left);
		}
	}
	return 0;
}

sub validmac
{
	$_ = $_[0];

	if (/^([0-9a-fA-F]{2}[\:\-]){5}[0-9a-fA-F]{2}$/) {
		return 1;
	}
	return 0;
}

sub validcomment
{
	$_ = $_[0];

	if (/^[\w\d\.\-,\(\)\@Â£\$!\%\^\&\*=\+_ ]*$/) {
		return 0 if ( length $_ > 255 );
		return 1;
	}
	return 0;
}


sub validhostname
{
	my $hostname = $_[0];
	my $part;

	# Sanity checks
	return 0 if (length($hostname) > 255);
	return 0 if ($hostname =~ /^[0-9.]+$/);
	return 0 unless ($hostname =~ /^[0-9A-Za-z][0-9A-Za-z._-]*[0-9A-Za-z]$/);

	my @parts = split(/\./, $hostname);
	# validate each label
	foreach $part (@parts) {
		return 0 if (length($part) > 63) ;
	}
	return 1;
}

sub validarchivename
{
	my $filename = $_[0];
	my $part;

	# Sanity checks
	# 43 bytes of template plus up to 63 bytes of simple hostname.
	return 0 if (length($filename) > 106);
	return 0 unless ($filename =~ /^[0-9A-Za-z._-]+$/);

	return 1;
}

sub basename {
	my ($filename) = @_;
	$filename =~ m!.*/(.*)!;

	if ($1) {
		return $1;
	}
	else {
		return $filename;
	}
}

sub dirname {
	my ($filename) = @_;
	$filename =~ s=(.*)/.*=$1=;

	if ($1) {
		return $1;
	}
	else {
		return $filename;
	}
}

sub connectedstate {
	my $locks = scalar(glob("/var/run/ppp-*.pid"));
	my $theconnstate;

	if ( -e "${swroot}/red/active" ) {
		$theconnstate = "connected";
	}
	elsif ($locks) {
		$theconnstate = "connecting";
	}
	else {
		$theconnstate = "idle";
	}
	return $theconnstate;
}

sub getsystemid
{
	my %ownership;
	&readhash("${swroot}/main/ownership", \%ownership);
	return $ownership{'ID'};
}

sub outputfile
{
	my $filename = $_[0];
	my $outfilename = $_[1];

	print "Content-type: application/octet-stream\n";
	print "Content-disposition: attachment; filename=\"$outfilename\"\n\n";

	open (FILE, $filename) or die "Unable to open $filename";
	while (<FILE>) {
		print $_;
	}
	close (FILE);
   
	exit;
}

sub getLinkSpeed
{
	# Return the specified NIC's formatted current speed or empty string
	my ($nic, $type) = @_;
	open(RATE, "/sys/class/net/$nic/speed");
	my $rate = <RATE>;
	chomp $rate;
	close RATE;

	if ($type eq "string") {
		return " ($rate)" if ($rate == 10 or $rate == 100 or $rate == 1000 or $rate == 10000);
		return "";
	}
	elsif ($type eq "number") {
		return "$rate" if ($rate == 10 or $rate == 100 or $rate == 1000 or $rate == 10000);
		return "0";
	}
	else {
		return undef;
	}
}

sub UTC2LocalString {
	use Time::Local;
	my $t = shift;

	# Return it unchanged if it's not the correct format
	return $t unless $t =~ /\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}:\d{2}/;

	my ($lDate, $lTime) = split (/\s+/,$t,2);
	my ($year, $month, $day) = split (/\//,$lDate);
	my ($hour, $minute, $sec) = split (/:/,$lTime);
  
	#  proto: $time = timegm($sec,$min,$hour,$mday,$mon,$year);
	my $UTCtime = timegm ($sec,$minute,$hour,$day,$month-1,$year);
  
	#  proto: ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
	my ($lsec,$lminute,$lhour,$lmday,$lmonth,$lyear,$lwday,$lyday,$lisdst) = (localtime($UTCtime));
  
	$lyear += 1900;  # year is 1900 based
	$lmonth++;       # month number is zero based
	#print "isdst: $isdst\n"; #debug flag day-light-savings time
	return ( sprintf("%4.4d/%2.2d/%2.2d %2.2d:%2.2d:%2.2d", $lyear, $lmonth, $lmday, $lhour, $lminute, $lsec) );
}

1;

