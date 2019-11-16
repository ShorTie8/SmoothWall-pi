#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team
#
# SmoothInfo MOD v. 2.2b by Pascal Touch  (nanouk) on Smoothwall forums (2008).
# SmoothInstall compatible
# Packed using Steve McNeill's Mod Build System
# Various tweaks to be 'strict' compliant and output valid W3C HTML. 

# debugging
#my $border = '1px solid';
my $border = 'none';

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothd qw( message );
use smoothtype qw(:standard);
use strict;
use warnings;

my (%smoothinfosettings, %checked, %selected, %netsettings);
my ($textarea, $bbcodehelp);

&readhash("${swroot}/ethernet/settings", \%netsettings );

my $MODDIR = "${swroot}/smoothinfo/etc";
my $filename = "$MODDIR/report.txt";
my $settingsfile = "$MODDIR/settings";
my @chains = ('All chains');
my @items = (
             'ADAPTERS',
             'APACHE',
             'CONFIG',
             'CONNTRACKS',
             'CPU',
             'DHCPINFO',
             'DISKSPACE',
             'DMESG',
             'DNS',
             'FWPOLICY',
             'IRQs',
             'LOADEDMODULES',
             'MEMORY',
             'MESSAGES',
             'MODLIST',
             'MODEXTRA',
             'NETCONF1',
             'NETCONF2',
             'OUTGOING',
             'PINHOLES',
             'PORTFW',
             'QOS',
             'ROUTE',
             'SERVICES',
             'SQUID',
             'TOP',
             'XTACCESS'
);
my @ASCII_items = ('SWITCH1', 'SWITCH2', 'SWITCH3', 'WAP1', 'WAP2', 'WAP3', 'WAP4', 'WAP5', 'WAP6', 'MODEM', 'ROUTER');

my $infomessage = '';
my $errormessage = '';

# Prepare @items for use as a JavaScript array
my $JSitems = "[\n";
foreach (@items){
	$JSitems .= "  '$_',\n";
}

chop($JSitems);
chop($JSitems);
$JSitems .= "\n]";

system ("/bin/touch","$settingsfile") unless (-e "$settingsfile");
system ("/bin/touch","$filename") unless (-e "$filename");

my $success = message('smoothinfogetchains');

$errormessage .= $tr{'smoothd failure'}. "<br />\n" unless ($success);

open (FILE, "<$MODDIR/chains");
@chains = (@chains,<FILE>);
chomp @chains;

# Prepare @chains for use as a JavaScript array
my $JSchains = "[\n";
foreach (@chains) {
	next if /All chains/;
	$JSchains .= "  '$_',\n";
}
chop($JSchains);
chop($JSchains);
$JSchains .= "\n]";

$smoothinfosettings{'ACTION'} = '';

foreach (@items, @ASCII_items, @chains) {
	$smoothinfosettings{$_} = 'off';
}

$smoothinfosettings{'HEADORTAIL'} = 'TAIL';
$smoothinfosettings{'HEADORTAIL2'} = 'TAIL2';
$smoothinfosettings{'HEADORTAIL3'} = 'TAIL3';
$smoothinfosettings{'LINES'} = '';
$smoothinfosettings{'LINES2'} = '';
$smoothinfosettings{'LINES3'} = '';
$smoothinfosettings{'STRING'} = '';
$smoothinfosettings{'STRING2'} = '';
$smoothinfosettings{'STRING3'} = '';
$smoothinfosettings{'SCREENSHOTS'} = '';
$smoothinfosettings{'WRAP'} = '100';
$smoothinfosettings{'NOSELECT'} = 'off';
$smoothinfosettings{'CHECKDEFAULT'} = 'off';
$smoothinfosettings{'CHECKALL'} = 'off';
$smoothinfosettings{'IGNORECASE'} = '';
$smoothinfosettings{'IGNORECASE2'} = '';
$smoothinfosettings{'IGNORECASE3'} = '';
$smoothinfosettings{'APACHE'} = '';
$smoothinfosettings{'MESSAGES'} = '';
$smoothinfosettings{'ALLCHAINS'} = 'off';
$smoothinfosettings{'EDIT'} = '';

&getcgihash(\%smoothinfosettings);

if ($smoothinfosettings{'ACTION'} eq $tr{'smoothinfo-generate'}) {
	# ERROR CHECKING
	my $msgOnce = 0;
	if ($smoothinfosettings{'LINES2'} eq '' &&
	    $smoothinfosettings{'STRING2'} eq '' &&
	    $smoothinfosettings{'APACHE'} eq 'on') {
		$msgOnce = 1;
		$errormessage .= $tr{'smoothinfo-define-number-of-lines'}. "<br />\n";
	}

	if ($smoothinfosettings{'LINES3'} eq '' &&
	    $smoothinfosettings{'STRING3'} eq '' &&
	    $smoothinfosettings{'MESSAGES'} eq 'on') {

		if ($msgOnce == 0) {
			$errormessage .= $tr{'smoothinfo-define-number-of-lines'}. "<br />\n";
		}
	}

	if ($smoothinfosettings{'SCREENSHOTS'} =~ /a href/i) {
		$errormessage .= $tr{'smoothinfo-bad-link'}. "<br />\n";
	}

	if ($smoothinfosettings{'SWITCH1'} eq 'on' ||
	    $smoothinfosettings{'SWITCH2'} eq 'on' ||
	    $smoothinfosettings{'SWITCH3'} eq 'on' ||
	    $smoothinfosettings{'WAP1'} eq 'on' ||
	    $smoothinfosettings{'WAP2'} eq 'on' ||
	    $smoothinfosettings{'WAP3'} eq 'on' ||
	    $smoothinfosettings{'WAP4'} eq 'on' ||
	    $smoothinfosettings{'WAP5'} eq 'on' ||
	    $smoothinfosettings{'WAP6'} eq 'on' ||
	    $smoothinfosettings{'MODEM'} eq 'on' ||
	    $smoothinfosettings{'ROUTER'} eq 'on') {
		system("/bin/touch $MODDIR/schematic");
	}
	else {
		unlink ("$MODDIR/schematic");
	}

	unless ( $smoothinfosettings{'ADAPTERS'} eq 'on' &&
		  $smoothinfosettings{'APACHE'} eq 'on' &&
		  $smoothinfosettings{'CONFIG'} eq 'on' &&
		  $smoothinfosettings{'CONNTRACKS'} eq 'on' &&
		  $smoothinfosettings{'CPU'} eq 'on' &&
		  $smoothinfosettings{'DHCPINFO'} eq 'on' &&
		  $smoothinfosettings{'DISKSPACE'} eq 'on' &&
		  $smoothinfosettings{'DMESG'} eq 'on' &&
		  $smoothinfosettings{'DNS'} eq 'on' &&
		  $smoothinfosettings{'FWPOLICY'} eq 'on' &&
		  $smoothinfosettings{'IRQs'} eq 'on' &&
		  $smoothinfosettings{'LOADEDMODULES'} eq 'on' &&
		  $smoothinfosettings{'MEMORY'} eq 'on' &&
		  $smoothinfosettings{'MESSAGES'} eq 'on' &&
		  $smoothinfosettings{'MODLIST'} eq 'on' &&
		  $smoothinfosettings{'MODEXTRA'} eq 'on' &&
		  $smoothinfosettings{'NETCONF1'} eq 'on' &&
		  $smoothinfosettings{'NETCONF2'} eq 'on' &&
		  $smoothinfosettings{'OUTGOING'} eq 'on' &&
		  $smoothinfosettings{'PINHOLES'} eq 'on' &&
		  $smoothinfosettings{'PORTFW'} eq 'on' &&
		  $smoothinfosettings{'QOS'} eq 'on' &&
		  $smoothinfosettings{'ROUTE'} eq 'on' &&
		  $smoothinfosettings{'SERVICES'} eq 'on' &&
		  $smoothinfosettings{'SQUID'} eq 'on' &&
		  $smoothinfosettings{'TOP'} eq 'on' &&
		  $smoothinfosettings{'XTACCESS'} eq 'on') {
		$smoothinfosettings{'CHECKALL'} = 'off';
	}

	unless ( $smoothinfosettings{'ADAPTERS'} eq 'on' ||
		  $smoothinfosettings{'APACHE'} eq 'on' ||
		  $smoothinfosettings{'CONFIG'} eq 'on' ||
		  $smoothinfosettings{'CONNTRACKS'} eq 'on' ||
		  $smoothinfosettings{'CPU'} eq 'on' ||
		  $smoothinfosettings{'DHCPINFO'} eq 'on' ||
		  $smoothinfosettings{'DISKSPACE'} eq 'on' ||
		  $smoothinfosettings{'DMESG'} eq 'on' ||
		  $smoothinfosettings{'DNS'} eq 'on' ||
		  $smoothinfosettings{'FWPOLICY'} eq 'on' ||
		  $smoothinfosettings{'IRQs'} eq 'on' ||
		  $smoothinfosettings{'LOADEDMODULES'} eq 'on' ||
		  $smoothinfosettings{'MEMORY'} eq 'on' ||
		  $smoothinfosettings{'MESSAGES'} eq 'on' ||
		  $smoothinfosettings{'MODLIST'} eq 'on' ||
		  $smoothinfosettings{'MODEXTRA'} eq 'on' ||
		  $smoothinfosettings{'NETCONF1'} eq 'on' ||
		  $smoothinfosettings{'NETCONF2'} eq 'on' ||
		  $smoothinfosettings{'OUTGOING'} eq 'on' ||
		  $smoothinfosettings{'PINHOLES'} eq 'on' ||
		  $smoothinfosettings{'PORTFW'} eq 'on' ||
		  $smoothinfosettings{'QOS'} eq 'on' ||
		  $smoothinfosettings{'ROUTE'} eq 'on' ||
		  $smoothinfosettings{'SERVICES'} eq 'on' ||
		  $smoothinfosettings{'SQUID'} eq 'on' ||
		  $smoothinfosettings{'TOP'} eq 'on' ||
		  $smoothinfosettings{'XTACCESS'} eq 'on') {
		$smoothinfosettings{'NOSELECT'} = 'on';
		$errormessage .= "$tr{'smoothinfo-nothing-selected'}<br />";
	}

	if ($smoothinfosettings{'CLIENTIP'} ne '') {
		open (TMP,">$MODDIR/clientip") || die 'Unable to open file';
		print TMP "$smoothinfosettings{'CLIENTIP'}";
		$smoothinfosettings{'CLIENTIP'} = '';
		close (TMP);
	}
	else {
		unlink ("$MODDIR/clientip");
	}

	open (OUT, ">",\$smoothinfosettings{'CHAINS'});
	foreach (@chains) {
		if ($smoothinfosettings{$_} eq 'on') {
			print OUT "$_,";
		}
	}

	if ($smoothinfosettings{'OTHER'} ne '') {
		if ($smoothinfosettings{'SECTIONTITLE'} eq '') {
			$errormessage .= $tr{'smoothinfo-no-section-title'}. "<br />\n";
		}
		open (TMP,">$MODDIR/otherinfo") || die 'Unable to open file';
		print TMP "$smoothinfosettings{'SECTIONTITLE'}\n";
		print TMP "$smoothinfosettings{'OTHER'}";
		$smoothinfosettings{'SECTIONTITLE'} = '';
		$smoothinfosettings{'OTHER'} = '';
		close (TMP);
	}
	else {
		unlink ("$MODDIR/otherinfo");
	}

	unless ($errormessage) {
		$smoothinfosettings{'data'} = '';
		$smoothinfosettings{'CHECKALL'} = '';
		$smoothinfosettings{'CHECKDEFAULT'} = '';
		foreach (@chains) {
			$smoothinfosettings{$_} = '';
		}
		&writehash("$settingsfile", \%smoothinfosettings);

		unless ($smoothinfosettings{'NOSELECT'} eq 'on') {
			my $success = message('smoothinfogenerate');
			$infomessage .= $success ."<br />\n" if ($success);
			$errormessage .= $tr{'smoothd failure'} ."<br />\n" unless ($success);
		}
	}

	if ($smoothinfosettings{'NOSELECT'} eq 'on') {
		open(FILE, ">/var/smoothwall/smoothinfo/etc/report.txt") or warn "Unable to open report file.";
		close FILE;
	}
}

&readhash("$settingsfile", \%smoothinfosettings);

$smoothinfosettings{'LINES'} = '';
$smoothinfosettings{'LINES2'} = '';
$smoothinfosettings{'LINES3'} = '';
$smoothinfosettings{'STRING'} = '';
$smoothinfosettings{'STRING2'} = '';
$smoothinfosettings{'STRING3'} = '';
$smoothinfosettings{'SCREENSHOTS'} = '';
$smoothinfosettings{'ALLCHAINS'} = 'off';


foreach (@items, @ASCII_items, @chains) {
	$checked{$_}{'off'} = '';
	$checked{$_}{'on'} = '';
	$checked{$_}{$smoothinfosettings{$_}} = 'CHECKED';
}

$checked{'EDIT'}{'off'} = '';
$checked{'EDIT'}{'on'} = '';
$checked{'EDIT'}{$smoothinfosettings{'EDIT'}} = 'CHECKED';

$checked{'CHECKDEFAULT'}{'off'} = '';
$checked{'CHECKDEFAULT'}{'on'} = '';
$checked{'CHECKDEFAULT'}{$smoothinfosettings{'CHECKDEFAULT'}} = 'CHECKED';

$checked{'CHECKALL'}{'off'} = '';
$checked{'CHECKALL'}{'on'} = '';
$checked{'CHECKALL'}{$smoothinfosettings{'CHECKALL'}} = 'CHECKED';

$checked{'ALLCHAINS'}{'off'} = '';
$checked{'ALLCHAINS'}{'on'} = '';
$checked{'ALLCHAINS'}{$smoothinfosettings{'ALLCHAINS'}} = 'CHECKED';

$checked{'DMESG'}{'off'} = '';
$checked{'DMESG'}{'on'} = '';
$checked{'DMESG'}{$smoothinfosettings{'DMESG'}} = 'CHECKED';

$checked{'APACHE'}{'off'} = '';
$checked{'APACHE'}{'on'} = '';
$checked{'APACHE'}{$smoothinfosettings{'APACHE'}} = 'CHECKED';

$checked{'MESSAGES'}{'off'} = '';
$checked{'MESSAGES'}{'on'} = '';
$checked{'MESSAGES'}{$smoothinfosettings{'MESSAGES'}} = 'CHECKED';

$checked{'IGNORECASE'}{'off'} = '';
$checked{'IGNORECASE'}{'on'} = '';
$checked{'IGNORECASE'}{$smoothinfosettings{'IGNORECASE'}} = 'CHECKED';

$checked{'IGNORECASE2'}{'off'} = '';
$checked{'IGNORECASE2'}{'on'} = '';
$checked{'IGNORECASE2'}{$smoothinfosettings{'IGNORECASE2'}} = 'CHECKED';

$checked{'IGNORECASE3'}{'off'} = '';
$checked{'IGNORECASE3'}{'on'} = '';
$checked{'IGNORECASE3'}{$smoothinfosettings{'IGNORECASE3'}} = 'CHECKED';

$selected{'HEADORTAIL'}{'HEAD'} = '';
$selected{'HEADORTAIL'}{'TAIL'} = '';
$selected{'HEADORTAIL'}{$smoothinfosettings{'HEADORTAIL'}} = 'CHECKED';

$selected{'HEADORTAIL2'}{'HEAD2'} = '';
$selected{'HEADORTAIL2'}{'TAIL2'} = '';
$selected{'HEADORTAIL2'}{$smoothinfosettings{'HEADORTAIL2'}} = 'CHECKED';

$selected{'HEADORTAIL3'}{'HEAD3'} = '';
$selected{'HEADORTAIL3'}{'TAIL3'} = '';
$selected{'HEADORTAIL3'}{$smoothinfosettings{'HEADORTAIL3'}} = 'CHECKED';

&showhttpheaders();

&openpage($tr{'smoothinfo-smoothinfo'}, 1, '', 'tools');

&openbigbox('100%', 'LEFT');
print <<END
<script type="text/javascript">

function toggle(Id)
{
	var el = document.getElementById(Id);
	if ( el.style.display != 'none' ) {
		el.style.display = 'none';
	}
	else {
		el.style.display = '';
	}
}

	
// Toggle the state of the arrow on the buttons.
//   Down when settings are hidden.
//   Up when they are visible.
// Ugly I admit :-( ...

function ToggleImage()
{
	downUrl = "url('/ui/img/down.jpg')";
	upUrl = "url('/ui/img/up.jpg')";

	if ( document.getElementById('A').style.display == 'none' ) {
		document.myform.SCHEMATIC.style.backgroundImage = downUrl;
		document.myform.SCHEMATIC.style.backgroundPosition = '97% 50%';
		document.myform.SCHEMATIC.style.backgroundRepeat = 'no-repeat';
		document.myform.SCHEMATIC.style.backgroundColor = '#cdcdcd';
		document.myform.SCHEMATIC.style.textAlign = 'left';
	}
	else {
		document.myform.SCHEMATIC.style.backgroundImage = upUrl;
		document.myform.SCHEMATIC.style.backgroundPosition = '97% 50%';
		document.myform.SCHEMATIC.style.backgroundRepeat = 'no-repeat';
		document.myform.SCHEMATIC.style.backgroundColor = '#cdcdcd';
		document.myform.SCHEMATIC.style.textAlign = 'left';
	}

	if ( document.getElementById('B').style.display == 'none' ) {
		document.myform.CLIENT.style.backgroundImage = downUrl;
		document.myform.CLIENT.style.backgroundPosition = '97% 50%';
		document.myform.CLIENT.style.backgroundRepeat = 'no-repeat';
		document.myform.CLIENT.style.backgroundColor = '#cdcdcd';
		document.myform.CLIENT.style.textAlign = 'left';
	}
	else {
		document.myform.CLIENT.style.backgroundImage = upUrl;
		document.myform.CLIENT.style.backgroundPosition = '97% 50%';
		document.myform.CLIENT.style.backgroundRepeat = 'no-repeat';
		document.myform.CLIENT.style.backgroundColor = '#cdcdcd';
		document.myform.CLIENT.style.textAlign = 'left';
	}

	if ( document.getElementById('C').style.display == 'none' ) {
		document.myform.IPTABLES.style.backgroundImage = downUrl;
		document.myform.IPTABLES.style.backgroundPosition = '97% 50%';
		document.myform.IPTABLES.style.backgroundRepeat = 'no-repeat';
		document.myform.IPTABLES.style.backgroundColor = '#cdcdcd';
		document.myform.IPTABLES.style.textAlign = 'left';
	}
	else {
		document.myform.IPTABLES.style.backgroundImage = upUrl;
		document.myform.IPTABLES.style.backgroundPosition = '97% 50%';
		document.myform.IPTABLES.style.backgroundRepeat = 'no-repeat';
		document.myform.IPTABLES.style.backgroundColor = '#cdcdcd';
		document.myform.IPTABLES.style.textAlign = 'left';
	}

	if ( document.getElementById('D').style.display == 'none' ) {
		document.myform.EXTRA.style.backgroundImage = downUrl;
		document.myform.EXTRA.style.backgroundPosition = '97% 50%';
		document.myform.EXTRA.style.backgroundRepeat = 'no-repeat';
		document.myform.EXTRA.style.backgroundColor = '#cdcdcd';
		document.myform.EXTRA.style.textAlign = 'left';
	}
	else {
		document.myform.EXTRA.style.backgroundImage = upUrl;
		document.myform.EXTRA.style.backgroundPosition = '97% 50%';
		document.myform.EXTRA.style.backgroundRepeat = 'no-repeat';
		document.myform.EXTRA.style.backgroundColor = '#cdcdcd';
	document.myform.EXTRA.style.textAlign = 'left';
	}
}

window.onload = function() { ToggleImage(); }

function CheckAll()
{
	var netState;
	var checkBoxes = ${JSitems};

	// Get the state
	var newState = document.myform.CHECKALL.checked;

	// Now set 'em all
	for (var myCheck in checkBoxes) {
		document.myform[checkBoxes[myCheck]].checked = newState;
	}

	// And turn back on the defaults, if that one's checked
	if (newState==false && document.myform.CHECKDEFAULT.checked) {
		CheckDef();
	}
}

function CheckDef()
{
	var checkBoxes = [
		'CONFIG',
		'DISKSPACE',
		'FWPOLICY',
		'MEMORY',
		'MODLIST',
		'NETCONF1',
		'NETCONF2',
		'QOS',
		'ROUTE',
		'SERVICES',
	];

	// Get the state
	var newState = document.myform.CHECKDEFAULT.checked;

	// Now set 'em all
	for (var myCheck in checkBoxes) {
		document.myform[checkBoxes[myCheck]].checked = newState;
	}
}

function CheckAllChains()
{
	var checkBoxes = ${JSchains};

	// Get the state
	var newState = document.myform.ALLCHAINS.checked;

	for (var myChain in checkBoxes) {
		document.myform[checkBoxes[myChain]].checked = newState;
	}
}

function SwitchOrWAP()
{
	var newState;
	var dmf = document.myform;
	// Schematic labels shortcuts
	var schLbls = {};
	schLbls.WAP1lbl = document.getElementById('WAP1lbl');
	schLbls.WAP2lbl = document.getElementById('WAP2lbl');
	schLbls.WAP3lbl = document.getElementById('WAP3lbl');
	schLbls.WAP4lbl = document.getElementById('WAP4lbl');
	schLbls.WAP5lbl = document.getElementById('WAP5lbl');
	schLbls.WAP6lbl = document.getElementById('WAP6lbl');
	schLbls.SWITCH1lbl = document.getElementById('SWITCH1lbl');
	schLbls.SWITCH2lbl = document.getElementById('SWITCH2lbl');
	schLbls.SWITCH3lbl = document.getElementById('SWITCH3lbl');

	// GREEN
	if (!(dmf.SWITCH1.checked) && !(dmf.WAP4.checked)) {
		dmf.SWITCH1.disabled = false;
		schLbls.SWITCH1lbl.style.color='#000000';
		dmf.WAP1.disabled = true;
		schLbls.WAP1lbl.style.color='#888888';
		dmf.WAP1.checked = false;
		dmf.WAP4.disabled = false;
		schLbls.WAP4lbl.style.color='#000000';
	}
	else if (dmf.SWITCH1.checked) {
		dmf.WAP1.disabled = false;
		schLbls.WAP1lbl.style.color='#000000';
		dmf.WAP4.disabled = true;
		schLbls.WAP4lbl.style.color='#888888';
	}
	else if (dmf.WAP4.checked) {
		dmf.SWITCH1.disabled = true;
		schLbls.SWITCH1lbl.style.color='#888888';
		dmf.WAP1.disabled = true;
		schLbls.WAP1lbl.style.color='#888888';
		dmf.WAP1.checked = false;
	}

	// ORANGE
	if (!(dmf.SWITCH2.checked) && !(dmf.WAP3.checked)) {
		dmf.SWITCH2.disabled = false;
		schLbls.SWITCH2lbl.style.color='#000000';
		dmf.WAP2.disabled = true;
		schLbls.WAP2lbl.style.color='#888888';
		dmf.WAP2.checked = false;
		dmf.WAP3.disabled = false;
		schLbls.WAP3lbl.style.color='#000000';
	}
	else if (dmf.SWITCH2.checked) {
		dmf.WAP2.disabled = false;
		schLbls.WAP2lbl.style.color='#000000';
		dmf.WAP3.disabled = true;
		schLbls.WAP3lbl.style.color='#888888';
	}
	else if (dmf.WAP3.checked) {
		dmf.SWITCH2.disabled = true;
		schLbls.SWITCH2lbl.style.color='#888888';
		dmf.WAP2.disabled = true;
		schLbls.WAP2lbl.style.color='#888888';
		dmf.WAP2.checked = false;
	}

	// PURPLE
	if (!(dmf.SWITCH3.checked) && !(dmf.WAP5.checked)) {
		dmf.SWITCH3.disabled = false;
		schLbls.SWITCH3lbl.style.color='#000000';
		dmf.WAP6.disabled = true;
		schLbls.WAP6lbl.style.color='#888888';
		dmf.WAP6.checked = false;
		dmf.WAP5.disabled = false;
		schLbls.WAP5lbl.style.color='#000000';
	}
	else if (dmf.SWITCH3.checked) {
		dmf.WAP6.disabled = false;
		schLbls.WAP6lbl.style.color='#000000';
		dmf.WAP5.disabled = true;
		schLbls.WAP5lbl.style.color='#888888';
	}
	else if (dmf.WAP5.checked) {
		dmf.SWITCH3.disabled = true;
		schLbls.SWITCH3lbl.style.color='#888888';
		dmf.WAP6.disabled = true;
		schLbls.WAP6lbl.style.color='#888888';
		dmf.WAP6.checked = false;
	}
}

function selectAll(field)
{
	var tempval=eval("document."+field);

	tempval.focus();
	tempval.select();
}
</script>

END
;

&alertbox($errormessage, "", $infomessage);

print <<END
<form method='POST' action='?' name='myform'><div>

<BR>
<table style='margin-left:auto; margin-right:auto; width: 95%; border:solid 1px; border-color:orange; background-color:#f9f0c7; padding:4px;'>
<tr>
	<td style='font-size:120%;'>$tr{'smoothinfo-caution'}</td>
</tr>
</table>

END
;

&openbox($tr{'smoothinfo-prepare-report'});

print<<END
<p class='base' style='vertical-align:middle; margin:1em 1em 0 1em; padding:4px;'>
	$tr{'smoothinfo-checkdefault'}
	<input type='checkbox' name='CHECKDEFAULT' $checked{'CHECKDEFAULT'}{'on'}
		style='display:inline-block; vertical-align:middle; margin:0'
		onClick='javaScript:CheckDef();'>
	&nbsp;&nbsp;&nbsp;&nbsp;
	$tr{'smoothinfo-checkall'}
	<input type='checkbox' name='CHECKALL' $checked{'CHECKALL'}{'on'}
		style='display:inline-block; vertical-align:middle; margin:0'
		onClick='javaScript:CheckAll();'>
	<span style='margin-left:10em'>
	$tr{'smoothinfo-wrap-prefix'}
	<input type='text' name='WRAP' value='$smoothinfosettings{'WRAP'}'
		size='5' style='display:inline-block;vertical-align:middle;margin:0'>
	$tr{'smoothinfo-wrap-suffix'}
	</span>
</p>
END
;

&openbox($tr{'smoothinfo-include'});

print <<END;
<table style='width:95%; margin-top:1em; margin-left:auto; margin-right:auto;'>
<tr>
	<th style='width:25%; padding:2px' colspan=2>$tr{'smoothinfo-sect-smoothwall'}</th>
	<th style='width:25%; padding:2px' colspan=2>$tr{'smoothinfo-sect-networking'}</th>
	<th style='width:25%; padding:2px' colspan=2>$tr{'smoothinfo-sect-firewall'}</th>
	<th style='width:25%; padding:2px' colspan=2>$tr{'smoothinfo-sect-services'}</th>
</tr>
<tr>
	<td class='base' TITLE='$tr{'smoothinfo-config-tip'}'>$tr{'smoothinfo-config'}:</td>
	<td style='width:3%;'><input type='checkbox' name='CONFIG' $checked{'CONFIG'}{'on'}></td>
	<td class='base' TITLE="$tr{'smoothinfo-net settings-tip'}">$tr{'smoothinfo-net settings'}:</td>
	<td style='width:3%;'><input type='checkbox' name='NETCONF2' $checked{'NETCONF2'}{'on'}></td>
	<td class='base' TITLE='$tr{'smoothinfo-conntracks-tip'}'>$tr{'smoothinfo-conntracks'}:</td>
	<td style='width:3%;'><input type='checkbox' name='CONNTRACKS' $checked{'CONNTRACKS'}{'on'}></td>
	<td class='base' TITLE='$tr{'smoothinfo-extra-tip'}'>$tr{'smoothinfo-extra-mods'}:</td>
	<td style='width:3%;'><input type='checkbox' name='MODEXTRA' $checked{'MODEXTRA'}{'on'}></td>
</tr>
<tr>
	<td class='base'>$tr{'smoothinfo-fwPolicy'}:</td>
	<td><input type='checkbox' name='FWPOLICY' $checked{'FWPOLICY'}{'on'}></td>
	<td class='base' TITLE='$tr{'smoothinfo-dhcpinfo-tip'}'>$tr{'smoothinfo-dhcpinfo'}:</td>
	<td><input type='checkbox' name='DHCPINFO' $checked{'DHCPINFO'}{'on'}></td>
	<td class='base'>$tr{'smoothinfo-external-access'}:</td>
	<td><input type='checkbox' name='XTACCESS' $checked{'XTACCESS'}{'on'}></td>
	<td class='base'>QoS:</td>
	<td><input type='checkbox' name='QOS' $checked{'QOS'}{'on'}></td>
</tr>
<tr>
	<td class='base' TITLE='$tr{'smoothinfo-mods-tip'}'>$tr{'smoothinfo-installed-mods'}:</td>
	<td><input type='checkbox' name='MODLIST' $checked{'MODLIST'}{'on'}></td>
	<td class='base'>$tr{'smoothinfo-dns'}:</td>
	<td><input type='checkbox' name='DNS' $checked{'DNS'}{'on'}></td>
	<td class='base'>$tr{'smoothinfo-portfw'}:</td>
	<td><input type='checkbox' name='PORTFW' $checked{'PORTFW'}{'on'}></td>
	<td class='base'>$tr{'smoothinfo-proxy'}:</td>
	<td><input type='checkbox' name='SQUID' $checked{'SQUID'}{'on'}></td>
</tr>
<tr>
	<td class='base' TITLE='$tr{'smoothinfo-services-status-tip'}'>$tr{'smoothinfo-services-status'}:</td>
	<td><input type='checkbox' name='SERVICES' $checked{'SERVICES'}{'on'}></td>
	<td class='base' TITLE='$tr{'smoothinfo-ifconfig-tip'}'>$tr{'smoothinfo-ifconfig'}:</td>
	<td><input type='checkbox' name='NETCONF1' $checked{'NETCONF1'}{'on'}></td>
	<td class='base'>$tr{'smoothinfo-internal-pinholes'}:</td>
	<td><input type='checkbox' name='PINHOLES' $checked{'PINHOLES'}{'on'}></td>
	<td></td>
	<td></td>
</tr>
<tr>
	<td></td>
	<td></td>
	<td class='base' TITLE='$tr{'smoothinfo-routes-tip'}'>$tr{'smoothinfo-routes'}:</td>
	<td><input type='checkbox' name='ROUTE' $checked{'ROUTE'}{'on'}></td>
	<td class='base'>$tr{'smoothinfo-outgoing-exceptions'}:</td>
	<td><input type='checkbox' name='OUTGOING' $checked{'OUTGOING'}{'on'}></td>
	<td></td>
	<td></td>
</tr>
<tr>
	<th style='padding:2px' colspan=8>$tr{'smoothinfo-sect-hardware'}</th>
</tr>
<tr>
	<td class='base' TITLE='$tr{'smoothinfo-adapters-tip'}'>$tr{'smoothinfo-adapters'}:</td>
	<td><input type='checkbox' name='ADAPTERS' $checked{'ADAPTERS'}{'on'}></td>
	<td class='base'>$tr{'smoothinfo-diskspace'}:</td>
	<td><input type='checkbox' name='DISKSPACE' $checked{'DISKSPACE'}{'on'}></td>
	<td class='base' TITLE='$tr{'smoothinfo-modules-tip'}'>$tr{'smoothinfo-modules'}:</td>
	<td><input type='checkbox' name='LOADEDMODULES' $checked{'LOADEDMODULES'}{'on'}></td>
	<td class='base' TITLE="$tr{'smoothinfo-top-tip'}">$tr{'smoothinfo-top'}:</td>
	<td><input type='checkbox' name='TOP' $checked{'TOP'}{'on'}></td>
</tr>
<tr>
	<td class='base'>$tr{'smoothinfo-cpu'}:</td>
	<td><input type='checkbox' name='CPU' $checked{'CPU'}{'on'}></td>
	<td class='base' TITLE='$tr{'smoothinfo-irqs-tip'}'>$tr{'smoothinfo-irqs'}:</td>
	<td><input type='checkbox' name='IRQs' $checked{'IRQs'}{'on'}></td>
	<td class='base' TITLE='$tr{'smoothinfo-memory-tip'}'>$tr{'smoothinfo-memory'}:</td>
	<td><input type='checkbox' name='MEMORY' $checked{'MEMORY'}{'on'}></td>
	<td></td>
	<td></td>
</tr>
</table>
END

&closebox();

&openbox("$tr{'smoothinfo-include-logsc'}&nbsp;&nbsp;&nbsp;<a href='#'><img src='/ui/img/help.gif' alt='?'
	title='$tr{'smoothinfo-log-help'}' style='vertical-align: text-top;' onclick=\"javascript:toggle('help'); return false;\"></a>");

print <<END;
<table style='width: 100%; margin-top:1em; padding: 0; border-spacing: 0; border: $border; margin-left:auto; margin-right:auto;'>
<tr>
	<td class='tightbase' TITLE='$tr{'smoothinfo-dmesg-tip'}'>$tr{'smoothinfo-dmesg'}</td>
	<td><input type='checkbox' name='DMESG' $checked{'DMESG'}{'on'}></td>
	<td class='tightbase'> $tr{'smoothinfo-head'}</td>
	<td><input type='radio' name='HEADORTAIL' value='HEAD' $selected{'HEADORTAIL'}{'HEAD'}></td>
	<td class='tightbase'>$tr{'smoothinfo-tail'}</td>
	<td><input type='radio' name='HEADORTAIL' value='TAIL' $selected{'HEADORTAIL'}{'TAIL'}></td>
	<td class='tightbase'><IMG SRC='/ui/img/blob.gif' ALT='*' style='vertical-align: text-top;'>&nbsp;$tr{'smoothinfo-lines'}</td>
	<td><input type='text' name='LINES' value='$smoothinfosettings{'LINES'}'
		size='2' TITLE='$tr{'smoothinfo-apache-lines-tip'}'></td>
	<td class='tightbase'><IMG SRC='/ui/img/blob.gif' ALT='*' style='vertical-align: text-top;'>&nbsp;$tr{'smoothinfo-search'}</td>
	<td><input type='text' name='STRING' value='$smoothinfosettings{'STRING'}' size='10'></td>
	<td class='tightbase'>$tr{'smoothinfo-ignore-case'}</td>
	<td><input type='checkbox' name='IGNORECASE' $checked{'IGNORECASE'}{'on'}></td>
</tr>
<tr style='background:#ecece8'>
	<td class='tightbase' TITLE='$tr{'smoothinfo-apache-error-tip'}'>$tr{'smoothinfo-apache-error'}</td>
	<td><input type='checkbox' name='APACHE' $checked{'APACHE'}{'on'}></td>
	<td class='tightbase'>$tr{'smoothinfo-head'}</td>
	<td><input type='radio' name='HEADORTAIL2' value='HEAD2' $selected{'HEADORTAIL2'}{'HEAD2'}></td>
	<td class='tightbase'>$tr{'smoothinfo-tail'}</td>
	<td><input type='radio' name='HEADORTAIL2' value='TAIL2' $selected{'HEADORTAIL2'}{'TAIL2'}></td>
	<td class='tightbase'><IMG SRC='/ui/img/blob.gif' ALT='*' style='vertical-align: text-top;'><IMG SRC='/ui/img/blob.gif' ALT='*' style='vertical-align: text-top;'>&nbsp;$tr{'smoothinfo-lines'}</td>
	<td><input type='text' name='LINES2' value='$smoothinfosettings{'LINES2'}' size='2' TITLE='$tr{'smoothinfo-apache-lines-tip'}'></td>
	<td class='tightbase'><IMG SRC='/ui/img/blob.gif' ALT='*' style='vertical-align: text-top;'><IMG SRC='/ui/img/blob.gif' ALT='*' style='vertical-align: text-top;'>&nbsp;$tr{'smoothinfo-search'}</td>
	<td><input type='text' name='STRING2' value='$smoothinfosettings{'STRING2'}' size='10'></td>
	<td class='tightbase'>$tr{'smoothinfo-ignore-case'}</td>
	<td><input type='checkbox' name='IGNORECASE2' $checked{'IGNORECASE2'}{'on'}></td>
</tr>
<tr>
	<td class='tightbase' TITLE='$tr{'smoothinfo-system-tip'}'>$tr{'smoothinfo-system'}</td>
	<td><input type='checkbox' name='MESSAGES' $checked{'MESSAGES'}{'on'}></td>
	<td class='tightbase'>$tr{'smoothinfo-head'}</td>
	<td><input type='radio' name='HEADORTAIL3' value='HEAD3' $selected{'HEADORTAIL3'}{'HEAD3'}></td>
	<td class='tightbase'>$tr{'smoothinfo-tail'}</td>
	<td><input type='radio' name='HEADORTAIL3' value='TAIL3' $selected{'HEADORTAIL3'}{'TAIL3'}></td>
	<td class='tightbase'><IMG SRC='/ui/img/blob.gif' ALT='*' style='vertical-align: text-top;'><IMG SRC='/ui/img/blob.gif' ALT='*' style='vertical-align: text-top;'>&nbsp;$tr{'smoothinfo-lines'}</td>
	<td><input type='text' name='LINES3' value='$smoothinfosettings{'LINES3'}' size='2' TITLE='$tr{'smoothinfo-apache-lines-tip'}'></td>
	<td class='tightbase'><IMG SRC='/ui/img/blob.gif' ALT='*' style='vertical-align: text-top;'><IMG SRC='/ui/img/blob.gif' ALT='*' style='vertical-align: text-top;'>&nbsp;$tr{'smoothinfo-search'}</td>
	<td><input type='text' name='STRING3' value='$smoothinfosettings{'STRING3'}' size='10'></td>
	<td class='tightbase'>$tr{'smoothinfo-ignore-case'}</td>
	<td><input type='checkbox' name='IGNORECASE3' $checked{'IGNORECASE3'}{'on'}></td>
</tr>
<tr>
	<td colspan='4' ><p class='base' style='margin:1em 0 0 1em'>
		<IMG SRC='/ui/img/blob.gif' ALT='*' style='vertical-align: text-top;'>&nbsp;$tr{'this field may be blank'}</p></td>
</tr>
<tr>
	<td colspan='4' style='margin-left:10pt'><p class='base' style='margin:.25em 0 0 1em'>
		<IMG SRC='/ui/img/blob.gif' ALT='*' style='vertical-align: text-top;'> <IMG SRC='/ui/img/blob.gif' ALT='*' style='vertical-align: text-top;'>
		&nbsp;$tr{'smoothinfo-both-fields-cannot-be-blank'}</p></td>
</tr>
</table>
END

print <<END;
<DIV Id='help' style='text-align:left; display: none;'>
<table style='width: 99%; border:dotted 1px; background-color:#ffee88; margin:0px; padding:4px;'>
<tr>
	<td style='width:15%; font-size:100%; font-style:italic;'>$tr{'smoothinfo-dmesg'}</td>
	<td style='font-size:100%;'>$tr{'smoothinfo-dmesg-help'}</td>
</tr>
<tr>
	<td style='width:15%; font-size:100%; font-style:italic;'>$tr{'smoothinfo-apache-error'}</td>
	<td style='font-size:100%;'>$tr{'smoothinfo-apache-error-help1'}</td>
</tr>
<tr>
	<td style='width:15%;'>&nbsp;</td>
	<td style='font-size:100%;'>$tr{'smoothinfo-apache-error-help2'}</td>
</tr>
<tr>
	<td style='width:15%; font-size:100%; font-style:italic;'>$tr{'smoothinfo-system'}</td>
	<td style='font-size:100%;'>$tr{'smoothinfo-system-log-help'}</td>
</tr>
</table>
</DIV>
END
;

&closebox();

&openbox($tr{'smoothinfo-other-informationc'});

&openbox($tr{'smoothinfo-include-screenshotsc'});

print <<END
<div style='margin:1em 0 0 1em;'>$tr{'smoothinfo-links-to-screenshotsc'}<br />
	<input type='text' name='SCREENSHOTS' value='$smoothinfosettings{'SCREENSHOTS'}'
	style='margin:.2em 0 0 2em;' size='74;' TITLE='$tr{'smoothinfo-screenshots-tip'}'></div>
END
;

&closebox();

print<<END;
<div style='text-align:center; margin:1em 1em .2em 1em'>
	<input type='button' name='SCHEMATIC' id='schematic'
		value='$tr{'smoothinfo-schematic'}&nbsp;&nbsp;&nbsp;&nbsp;' style='margin:0 .1em'
		onClick="javascript:toggle('A'); javascript:ToggleImage();" />
	<input type='button' name='CLIENT' id='client'
		value='$tr{'smoothinfo-clientinfo'}&nbsp;&nbsp;&nbsp;&nbsp;' style='margin:0 .1em'
		onClick="javascript:toggle('B'); javascript:ToggleImage();" />
	<input type='button' name='IPTABLES' id='iptables'
		value='$tr{'smoothinfo-iptables'}&nbsp;&nbsp;&nbsp;&nbsp;' style='margin:0 .1em'
		onClick="javascript:toggle('C'); javascript:ToggleImage();" />
	<input type='button' name='EXTRA' id='other'
		value='$tr{'smoothinfo-other'}&nbsp;&nbsp;&nbsp;&nbsp;' style='margin:0 .1em'
		onClick="javascript:toggle('D'); javascript:ToggleImage();" />
</div>
END
;

print <<END
<DIV Id='A' style="display:none;">
END
;

&openbox();

#RED '#ffaaaa'; }
#"Green") {$bgcolor = "#bbffbb";}
#"Purple") {$bgcolor = "#ddaaff";}
#"Orange") {$bgcolor = "#ffaa77";}

print <<END
<b>$tr{'smoothinfo-shematic-items'}</b>

<table width='inherit' style='margin:1em 2em 0 2em'>
<tr>
	<td rowspan='7' style='margin:0; width:8.6em; text-align:center; background-color:white; border:solid black .2em'>
		<b>SMOOTHWALL</b></td>

	<td style='margin:0; padding:.3em; height:3em; background-color:#bbffbb; vertical-align:middle; border: solid black .2em'>
	   <div style='vertical-align:middle; text-align:left; margin:0'>
		<span style='color:#bbffbb'><i>(GREEN)</i> &harr;</span>
		<input type='checkbox' name='WAP4' $checked{'WAP4'}{'on'}
			onClick='javaScript:SwitchOrWAP();' /><b><span id='WAP4lbl'>WAP</span></b> &harr; W/Lan<br />
		<i>(GREEN)</i> &harr;
		<input type='checkbox' name='SWITCH1' $checked{'SWITCH1'}{'on'}
			onClick='javaScript:SwitchOrWAP();' /><b><span id='SWITCH1lbl'>Switch</span></b> &harr; LAN &harr;
		<input type='checkbox' name='WAP1' $checked{'WAP1'}{'on'}
			onClick='javaScript:SwitchOrWAP();' /><b><span id='WAP1lbl'>WAP</span></b> &harr; W/Lan
	   </div></td>
</tr>
<tr>
	<td style='font-size:18pt'>&nbsp;</td>
</tr>
END
;

if ($netsettings{'ORANGE_DEV'}) {
	print <<END
<tr>
	<td style='margin:0; padding:.3em; height:3em; background-color:#ffaa77; vertical-align:middle; border: solid black .2em'>
	   <div style='vertical-align:middle; text-align:left; margin:0'>
		<span style='color:#ffaa77'><i>(ORANGE)</i> &harr;</span>
		<input type='checkbox' name='WAP3' $checked{'WAP3'}{'on'}
			onClick='javaScript:SwitchOrWAP();' /><b><span id='WAP3lbl'>WAP</span></b> &harr; W/Lan<br />
		<i>(ORANGE)</i> &harr;
		<input type='checkbox' name='SWITCH2' $checked{'SWITCH2'}{'on'}
			onClick='javaScript:SwitchOrWAP();' /><b><span id='SWITCH2lbl'>Switch</span></b> &harr; LAN &harr;
		<input type='checkbox' name='WAP2' $checked{'WAP2'}{'on'}
			onClick='javaScript:SwitchOrWAP();' /><b><span id='WAP2lbl'>WAP</span></b> &harr; W/LAN
	   </div></td>
</tr>
<tr>
	<td style='font-size:18pt'>&nbsp;</td>
</tr>
END
;
}

if ($netsettings{'PURPLE_DEV'}) {
	print <<END
<tr>
	<td style='margin:0; padding:.3em; height:3em; background-color:#ddaaff; vertical-align:middle; border: solid black .2em'>
	   <div style='vertical-align:middle; text-align:left; margin:0'>
		<span style='color:#ddaaff'><i>(PURPLE)</i> &harr;</span>
		<input type='checkbox' name='WAP5' $checked{'WAP5'}{'on'}
			onClick='javaScript:SwitchOrWAP();' /><b><span id='WAP5lbl'>WAP</span></b> &harr; W/Lan<br />
		<i>(PURPLE)</i> &harr;
		<input type='checkbox' name='SWITCH3' $checked{'SWITCH3'}{'on'}
			onClick='javaScript:SwitchOrWAP();' /><b><span id='SWITCH3lbl'>Switch</span></b> &harr; LAN &harr;
		<input type='checkbox' name='WAP6' $checked{'WAP6'}{'on'}
			onClick='javaScript:SwitchOrWAP();' /><b><span id='WAP6lbl'>WAP</span></b> &harr; W/LAN
	   </div></td>
</tr>
<tr>
	<td style='font-size:18pt'>&nbsp;</td>
</tr>
END
;
}
print <<END
<tr>
	<td style='margin:0; padding:.3em; height:3em; background-color:#ffaaaa; vertical-align:middle; border: solid black .2em'>
	   <div style='vertical-align:middle; text-align:left; margin:0'>
		<i>(RED)</i> &harr;
		<input type='checkbox' name='ROUTER' $checked{'ROUTER'}{'on'}><b>Router</b> &harr; LAN &harr;
		<input type='checkbox' name='MODEM' $checked{'MODEM'}{'on'}><b>Modem</b> &harr; Internet
	   </div></td>
</tr>
</table>
<script type="text/javascript">SwitchOrWAP();</script>
END
;

&closebox();
print <<END
</DIV>
END
;

print <<END
<DIV Id='B' style="display:none;">
END
;

&openbox();
print <<END
<b>$tr{'smoothinfo-clientIP'}</b>
<BR><BR>
<div style='color:red; text-align:center;'>$tr{'smoothinfo-warn'}</div>
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width: 9%; text-align:center;'><TEXTAREA name='CLIENTIP' ROWS='10' COLS='70' style='white-space: pre; word-wrap: normal; overflow-x: scroll;' TITLE='$tr{'smoothinfo-clientIP-tip'}'>
</TEXTAREA></td>
</tr>
</table>
END
;
&closebox();
print <<END
</DIV>
END
;

print <<END
<DIV Id='C' style="display:none;">
END
;

&openbox($tr{'smoothinfo-known-chains'});
print "$tr{'smoothinfo-chains'}";
my @rows = ();
print "<table style='width: 100%;'>";
my $id = -1;
foreach (@chains) {
	$id++;
	if (/All chains/) {
		push @rows, qq[<td style='width: 15%; color: red; font-weight: bold;'>$_</td>
	<td style='width: 20%;'><input type='checkbox' name='ALLCHAINS' $checked{'ALLCHAINS'}{'on'} onClick='javaScript:CheckAllChains();' /></td>\n];
	}
	else {
		push @rows, qq[<td style='width: 15%;'>$_</td><td style='width: 20%;'><input type='checkbox' name="$_" $checked{"$_"}{'on'}></td>\n];
	}
}

# 3columns
for(my $id = 0; $id <= $#rows; $id += 3) {
	$rows[$id+1] = '' unless defined $rows[$id+1];
	$rows[$id+2] = '' unless defined $rows[$id+2];
	print "<tr>" . $rows[$id] . $rows[$id+1] . $rows[$id+2] . "</tr>\n";
}
print "</table>";
&closebox();

print <<END
</DIV>
END
;

print <<END
<DIV Id='D' style="display:none;">
END
;
&openbox("$tr{'smoothinfo-other'}:");
print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width: 9%;'><b>$tr{'smoothinfo-other-title'}</b></td>
	<td style='width: 91%;'><input type='text' name='SECTIONTITLE' Id='sectiontitle' value='$smoothinfosettings{'SECTIONTITLE'}'  
		@{[jsvalidregex('sectiontitle','^[a-zA-Z0-9-_., ]+$')]} size='20'>&nbsp;<i>(required)</i></td>
</tr>
</table>
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width: 50%; text-align:center;'>
		<TEXTAREA name='OTHER' ROWS='10' COLS='70' style='white-space: pre; word-wrap: normal; overflow-x: scroll;' TITLE='$tr{'smoothinfo-other-tip'}'>
		</TEXTAREA></td>
</tr>
</table>
END
;
&closebox();
print <<END
</DIV>
END
;

&closebox();

&closebox();

print <<END
<table style='width: 60%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='text-align:center;'><input type='submit' name='ACTION' value='$tr{'smoothinfo-generate'}' style="height:25px;background-color:#fdb445;font: bold 12px Arial;" onClick="return confirm('$tr{'smoothinfo-confirm'}');"></td>
</tr>
</table>
END
;

if ($smoothinfosettings{'EDIT'} eq 'on') {
	$textarea = "<td style='width:50%; text-align:center;'><TEXTAREA name='data' ROWS='30' COLS='85' style='white-space: pre; word-wrap: normal; overflow-x: scroll;'>";
	$bbcodehelp = "<td style='text-align:right; font-style: italic; font-size:small; vertical-align: super;'>
		<A HREF='http://community.smoothwall.org/forum/faq.php?mode=bbcode' 
		onclick=\"window.open(this.href,'popup','height=600 ,width=800, scrollbars=yes, left=150,top=150,screenX=150,screenY=150');return false;\" 
		TITLE='$tr{'smoothinfo-connected'}'>$tr{'smoothinfo-bbcode'}&nbsp;</a></td>";
}
else {
	$textarea = "<td style='width:50%; text-align:center;'><TEXTAREA name='data' ROWS='30' COLS='85' style='white-space: pre; word-wrap: normal; overflow-x: scroll; background:#ecece8' READONLY TITLE='$tr{'smoothinfo-report-tip'}' onclick='this.select();'>";
	$bbcodehelp = '';
}

&openbox($tr{'smoothinfo-report'});
print <<END
<table style='width: 60%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td class='base' style='text-align:left;' TITLE='$tr{'smoothinfo-edit-tip'}'>$tr{'smoothinfo-edit'}&nbsp;<input type='checkbox' name='EDIT' $checked{'EDIT'}{'on'}></td>
	$bbcodehelp
</tr>
</table>

<table style='width: 60%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='text-align:center;'><a href="javascript:selectAll('myform.data')" style='font-size:120%; color:red; font-weight:bold;' TITLE='$tr{'smoothinfo-selectall-tip'}'>$tr{'smoothinfo-selectall'}</a></td>
</tr>
</table>

<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
$textarea
END
;

open (REPORT, "<$filename") or die "unable to open report";
while (<REPORT>) {
	chomp;
	print "$_\n";
}
close REPORT;

print <<END
</TEXTAREA></td>
</tr>
</table>
<BR>
END
;
&closebox();

print "</div></form>\n";

&closebigbox();
&closepage();
