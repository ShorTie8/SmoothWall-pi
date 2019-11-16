# SmoothWall Express "Types" Module
#
# This code is distributed under the terms of the GPL
#
# (c) 2004-2007 SmoothWall Ltd

package smoothtype;
require Exporter;
@ISA = qw(Exporter);

use header qw(:standard);

# define the Exportlists.

@EXPORT       = qw();
@EXPORT_OK    = qw( 
	ipcompare
	portmap
	tooltip portlist displaytable dispaliastab
	jsvalidip jsvalidmask jsvalidipormask jsvalidipandmask jsvalidport jsvalidportrange jsvalidmac jsvalidhostname jsvalidregex jsvalidpassword jsvalidnumber jsvalidcomment
	);
%EXPORT_TAGS  = (
	standard   => [@EXPORT_OK],
	);

sub tooltip
{
	my ( $tip, $options ) = @_;
	my $oplist;

	foreach my $option ( keys %$options ) {
		$oplist .= "this.$option = '$options->{$option}';";
	}		
	return "onMouseOver=\"$oplist return escape( $tip );\"";
}

my $files = "/var/smoothwall/knownports/*";

sub portmap
{
	my %ports;
	
	foreach my $filename ( glob $files ) {
		next unless (open(FILE, $filename));

		while ( my $line = <FILE> ) {
			chomp $line;
			next if ( $line eq "" );
	
			my ( $name, $value ) = split /,/, $line;

			$ports{$value} = "$name ($value)";
		}
	}
	return \%ports;
}

sub portlist
{
	my ( $selectfield, $selectfieldname, $inputfield, $inputfieldname, $chosen, $options ) = @_; 
	my %ports;

	my $ungrouped = $options->{'ungrouped'};
	my $allowblank = $options->{'blank'};
	my $blob = $options->{'blob'};
	
	my $blobgif;
	$blobgif = '<img src=\'/ui/img/blob.gif\' alt=\'*\'>&nbsp;' if ($blob eq 'true');

	$allowblank = 'false' if ( not defined $allowblank or $allowblank ne 'true' );

	foreach my $filename ( glob $files ) {
		next unless (open(FILE, $filename));

		my ( $section ) = ( $filename =~/([^\/]*)$/i );

		while ( my $line = <FILE> ) {
			chomp $line;
			next if ( $line eq "" );

			my ( $name, $value ) = split /,/, $line;
	
			$ports{$section}{$name} = $value;
		}
	
		close FILE;
	}

	my $response = qq{
	<td class='base'>$selectfieldname</td>
	<td><select name='$selectfield' id='$selectfield' onChange="portlist('$selectfield','$inputfield','user',$allowblank);">
		<option value='user'>$tr{'user defined'}</option>
	};

	my $found = $chosen;
	$found = "" if ( $chosen eq "user" );

	foreach my $key ( keys %{$ports{'main'}} ) {
		if ( $chosen eq $key ) {
			$response .= "<option value='$ports{'main'}{$key}' selected>$key ($ports{'main'}{$key})</option>\n";
			$found = "";
		}
		else {
			$response .= "<option value='$ports{'main'}{$key}'>$key ($ports{'main'}{$key})</option>\n";
		}
	}

	foreach my $section ( keys %ports ) {
		next if ( $section eq 'main' );

		my $precursor = "";

		if ( not defined $ungrouped ) {
			if ( $chosen eq $section ) {
				$response .= "<option selected value='$section'>$section</option>\n";
				$found = "";
			}
			else {
				$response .= "<option value='$section'>$section</option>\n";
			}
			$precursor = " - ";
		}
		foreach my $key ( keys %{$ports{$section}} ) {
			if ( $chosen eq $ports{$section}{$key} ) {
				$response .= "<option selected value='$ports{$section}{$key}'>$precursor$key ($ports{$section}{$key})</option>\n";
				$found = "";
			}
			else {
				$response .= "<option value='$ports{$section}{$key}'>$precursor$key ($ports{$section}{$key})</option>\n";
			}
		}
	}

	$response .= qq{
	</select></td>
	<td class='base'><img src=\'/ui/img/blob.gif\' alt=\'*\'>&nbsp;$inputfieldname</td>
	<td><input type='text' id='$inputfield' name='$inputfield' @{[script("validport('$inputfield', $allowblank);")]} value='$found'/></td>
	};

	
	push @_validation_items, "validport('$inputfield', $allowblank)" ;
	push @_validation_items, "portlist('$selectfield','$inputfield','user', $allowblank)" ;

	return $response;
}

sub script
{
	my ($script) = @_;
	my @event_handlers = ( "onKeyUp", "onFocus", "onBlur", "onChange" );

	my $val = "";
	foreach my $handler ( @event_handlers ) {
		$val .= " $handler=\"$script\" ";
	}
	
	return $val;
}


# Common UI Elements 
# Sortable Tables of Settings ....

sub displaytable
{
	my ( $filename, $settings, $order, $selected_column, $id ) = @_;

	# 'id' can be used to give us a different name, *iff* we are repeating the
	# widget. If it isn't set, set it randomly.
	if (! defined($id) || $id eq "") {
		$id = rand(1000);
	}

	print qq{
		<table class='list' style='margin:6pt auto'>
		<tr>
	};

	# display the header information, that is the list of columns etc.
	# whilst we're doing this, we can generate a mapping of which column to 
	# display where.

	my @columns;
	my @styles;
	my @translations;
	my @breaks;
	my @urls;

	my $i = 0;
	my $sort;
	my $colourtranslations;
	my $colourcolumn = 0;
	my $colcount;
	my $headerrowspan = 0;

	#my ( $table1colour, $table2colour ) = ( '#f0f0f0', '#e0e0e0' );
	my ( $table1colour, $table2colour ) = ( "rgba(0,0,0,.03)", "rgba(0,0,0,.1)" );


	foreach my $column ( @{$settings->{'columns'}} ){
		my $span = "";
		my $style = "background-color: $table1colour;";
		my $class = "list";

		if ( defined $column->{'maxrowspan'} ) {
			$rowspan = " rowspan='$column->{'maxrowspan'}'";
			$headerrowspan = 1;
		}
		else {
			$rowspan = "";
		}

		if ( defined $column->{'rotate'} ) {
			$rotate = "; transform:rotate($column->{'rotate'}deg);";
			if ( defined $column->{'valign'} ) {
				$style .= "vertical-align:middle;";
			}
		}
		else {
			$rotate = "";
			if ( defined $column->{'valign'} ) {
				$style .= "vertical-align:bottom;";
			}
		}

		if ( defined $column->{'align'} ) {
			$style .= "text-align: $column->{'align'};";
		}

		if ( defined $column->{'break'} ) {
			print "</tr><tr>";
			$colcount = scalar(@columns) + $column->{'spanadj'};
			$span = " colspan='$colcount'";
			$class = "listcomment";
		}
		else {
			$style .= "border-bottom:1px solid #d0d0d0;";
		}

		if ( $rotate eq "" ) {
			if ( defined $column->{'size'} ){
				$style .= "width: $column->{'size'}%;";
			}
		}
		else {
			$style .= "width:.01%; height:6em;";
		}

		my $arrow;
		my $url = $settings->{'url'};
		$i++;
		$url =~s/\[%COL%\]/$i/;		

		if ( $i == $selected_column ) {
			if ( $order eq $tr{'log ascending'} ) {
				$url =~s/\[%ORD%\]/$tr{'log descending'}/;
				$arrow = "&nbsp;<img src='/ui/img/down.jpg' alt='change direction'>";
			}
			else {
				$url =~s/\[%ORD%\]/$tr{'log ascending'}/;
				$arrow = "&nbsp;<img src='/ui/img/up.jpg' alt='change direction'>";
			}

			# choose a sorting algorithm
			if ( defined $column->{'sort'} ) {
				$sort = $column->{'sort'};
			}

		}
		else {
			$url =~s/\[%ORD%\]/$tr{'log ascending'}/;
		}

		if ( not defined $column->{'colour'} ) {
			print qq !
		<th$span$rowspan class='$class' style='$style; padding:.05em .5em'>
			<div style="a$rotate"><a href="$url">$column->{'title'}$arrow</a></div></th>
!;
		}

		$style = "";

		if ( defined $column->{'align'} ) {
			$style .= "text-align: $column->{'align'};";
		}

		if ( defined $column->{'break'} ) {
			push @breaks, $column->{'column'};
		}
		elsif ( defined $column->{'urllimit'} ) {
			push @urls,  $column->{'column'};
		}
		elsif ( defined $column->{'colour'} ) {
			$colourcolumn = $column->{'column'};
			$colourtranslations = $column->{'tr'};
		}
		else {
			# In case no column has been specified, assume column 0.
			if ( not defined $column->{'column'} ) {
				push @columns, "0,$column->{'mark'}";
			}
			elsif ( defined $column->{'mark'} ) {
				push @columns, "$column->{'column'},$column->{'mark'}";
			}
			else {
				push @columns, $column->{'column'};
			}
		}
		push @styles, $style;
		push @translations, $column->{'tr'};
	}
	
	print qq{
		</tr>
	};

	# now we can render the content

	my $colour = "background-color: $table2colour;";
	$i = 0;
	my @lines;

	if (ref($filename) eq "ARRAY") {
		foreach $line (@$filename) {
			my @cols;
			if ($line =~ /\|/) {
				@cols = ( $position++, (split /\|/, $line) );
			}
			else {
				@cols = ( $position++, (split / /, $line) );
			}
			push @lines, \@cols;
		}
	}
	elsif ( open my $input, "$filename" ) {
		my $position = 1;
		while( my $line = <$input> ) {
			chomp $line;
			my @cols = ( $position++, (split /,/, $line) );
			push @lines, \@cols;
		}
		close $input;
	}
	else {
		print "</table>\n";
		return;
	}
	
	# sort the lines according to the relevant selected row.
	my @sorted_lines;

	if ( ref $sort ) {
		# an overridden sort function.
		if ( $order eq $tr{'log ascending'} ) {
			@sorted_lines = sort { &{$sort}( $a->[$columns[$selected_column-1]], $b->[$columns[$selected_column-1]] ) } @lines;
		}
		else {
			@sorted_lines = sort { &{$sort}( $b->[$columns[$selected_column-1]], $a->[$columns[$selected_column-1]] ) } @lines;
		}
	} elsif ( $sort eq "<=>" ) {
		if ( $order eq $tr{'log ascending'} ) {
			@sorted_lines = sort { $a->[$columns[$selected_column-1]] <=> $b->[$columns[$selected_column-1]] } @lines;
		}
		else {
			@sorted_lines = sort { $b->[$columns[$selected_column-1]] <=> $a->[$columns[$selected_column-1]] } @lines;
		}
	}
	else {
		if ( $order eq $tr{'log ascending'} ) {
			@sorted_lines = sort { $a->[$columns[$selected_column-1]] cmp $b->[$columns[$selected_column-1]] } @lines;
		}
		else {
			@sorted_lines = sort { $b->[$columns[$selected_column-1]] cmp $a->[$columns[$selected_column-1]] } @lines;
		}	
	}

	# slice the information up at all ?
	my $sliced = 0;

	if ( defined $settings->{'slice'} and ref $settings->{'slice'} ) {
		my $start = $settings->{'slice'}->{'start'};
		my $end   = $settings->{'slice'}->{'end'};
		$sliced   = scalar @sorted_lines;
		my @slice = splice( @sorted_lines, $start, $end);
		@sorted_lines = @slice;
	}

	foreach my $line (@sorted_lines) {
		my @cols = @{$line};
		print "<tr class='list'>\n";
		my $entry = 0;
		my $rowspan = "";
		# Each comment increments $rowSpanCount
		$rowSpanCount = 1;
		foreach my $reference ( @breaks ){
			if ( defined $cols[$reference] and $cols[$reference] ne "" ) {
				$rowSpanCount++;
			}
		}
		if ($headerrowspan == 1 and $rowSpanCount > 1) {
			$rowspan = " rowspan='$rowSpanCount'";
		}
		foreach my $reference ( @columns ) {
			unless ( $reference =~ /,/ ) {
				# are we supposed to translate this at all ?
				my $text = $cols[$reference];
				if ( defined $translations[$entry] ) {
					my $type = ref $translations[$entry];
					if ( not $type ) {
						if ( $translations[$entry] eq "onoff" ) {
							if ( $cols[$reference] eq "on" ) {
								$text = "<img alt='on' src='/ui/img/on.gif'>";
							}
							else {
								$text = "<img alt='off' src='/ui/img/off.gif'>";
							}
						}
						if ( $translations[$entry] =~ /url/ ) {
							my ($kwd, $charlimit) = split (/:/, $translations[$entry]);
							my $url = $text;
							my $part = substr($text, 0, 80);
							$part .= "..." unless length($part) < 80;
							$text = "<a href='$url' title='$url' target='_new'>";
							$text .= "$part</a>";
						}
					}
					elsif ( $type eq "HASH" and defined $translations[$entry]->{$cols[$reference]} ){
						$text = $translations[$entry]->{$cols[$reference]};
					}
					elsif ( $type eq "ARRAY" and defined $translations[$entry]->[$cols[$reference]] ){
						$text = $translations[$entry]->[$cols[$reference]];
					}
				}
				if ( $colourcolumn != 0 ) {
					$text = "<span class='$colourtranslations->{$cols[$colourcolumn]}'>$text</span>";
				}
				print "<td$rowspan class='list' style='$colour$styles[$entry]; padding:.1em .5em'><p style='margin:0'>$text</p></td>\n";
				# Single use!
				$rowspan = "";

			}
			else {
				# this is a "mark" field, i.e. a checkbox
				my $text;
				my ($column, $mark) = split( /,/, $reference );
				my $newmark = "";
				if ( $mark ne " " ) {
					$newmark = $mark;
				}
				print "<td class='list' style='$colour$styles[$entry]' onclick=\"toggle_mark('R${id}_$cols[0]');\"><input id ='R${id}_$cols[$column]' type='checkbox' name='$newmark$cols[$column]' onclick=\"toggle_mark('R${id}_$cols[0]');\"></td>";
			}
			$entry++;
		}

		# do we need to render any comments etc ?
		foreach my $reference ( @breaks ){
			if ( defined $cols[$reference] and $cols[$reference] ne "" ) {
				print "</tr><tr class='list'><td style='padding:.1em .5em; $colour $styles[$entry]' class='listcomment' colspan='$colcount'><i>$cols[$reference]</i></td>\n";
			}
		}

		$i++;
		print "</tr>\n";
		if ( $colour eq "background-color: $table1colour;" ) {
			$colour = "background-color: $table2colour;";
		}
		else {
			$colour = "background-color: $table1colour;";
		}
	}
	

	# and end the table
	print qq{
		</table>
	};

}


sub dispaliastab
{
	my ( $filename, $settings, $order, $selected_column, $id ) = @_;

	# 'id' can be used to give us a different name, *iff* we are repeating the
	# widget. If it isn't set, set it randomly.
	if (! defined($id) || $id eq "") {
		$id = rand(1000);
	}

	print qq{
		<table class='list' style='margin:6pt auto'>
			<tr>
	};

	# display the header information, that is the list of columns etc.
	# whilst we're doing this, we can generate a mapping of which column to 
	# display where.

	my @columns;
	my @styles;
	my @translations;
	my @breaks;
	my @urls;

	my $i = 0;
	my $sort;
	my $colourtranslations;
	my $colourcolumn = 0;
	my $colcount;
	my $headerrowspan = 0;

	my ( $table1colour, $table2colour ) = ( '#f0f0f0', '#e0e0e0' );

	foreach my $column ( @{$settings->{'columns'}} ) {
		my $span = "";
		my $style = "background-color: $table1colour;";
		my $class = "list";

		if ( defined $column->{'maxrowspan'} ) {
			$rowspan = " rowspan='$column->{'maxrowspan'}'";
			$headerrowspan = 1;
		}
		else {
			$rowspan = "";
		}

		if ( defined $column->{'rotate'} ) {
			$rotate = "; transform:rotate($column->{'rotate'}deg);";
			if ( defined $column->{'valign'} ) {
				$style .= "vertical-align:middle;";
			}
		}
		else {
			$rotate = "";
			if ( defined $column->{'valign'} ) {
				$style .= "vertical-align:bottom;";
			}
		}

		if ( defined $column->{'align'} ) {
			$style .= "text-align: $column->{'align'};";
		}

		if ( defined $column->{'break'} ) {
			print "</tr><tr>";
			$colcount = scalar(@columns) + $column->{'spanadj'};
			$span = " colspan='$colcount'";
			$class = "listcomment";
		}
		else {
			$style .= "border-bottom:1px solid #d0d0d0;";
		}

		if ( $rotate eq "" ) {
			if ( defined $column->{'size'} ) {
				$style .= "width: $column->{'size'}%;";
			}
		}
		else {
			$style .= "width:.01%; height:6em;";
		}

		my $arrow;
		my $url = $settings->{'url'};
		$i++;
		$url =~s/\[%COL%\]/$i/;		

		if ( $i == $selected_column ) {
			if ( $order eq $tr{'log ascending'} ) {
				$url =~s/\[%ORD%\]/$tr{'log descending'}/;
				$arrow = "&nbsp;<img src='/ui/img/down.jpg' alt='change direction'>";
			}
			else {
				$url =~s/\[%ORD%\]/$tr{'log ascending'}/;
				$arrow = "&nbsp;<img src='/ui/img/up.jpg' alt='change direction'>";
			}

			# choose a sorting algorithm
			if ( defined $column->{'sort'} ) {
				$sort = $column->{'sort'};
			}

		}
		else {
			$url =~s/\[%ORD%\]/$tr{'log ascending'}/;
		}

		if ( not defined $column->{'colour'} ) {
			print qq !
				<th$span$rowspan class='$class' style='$style; padding:.05em .5em'>
					<div style="a$rotate"><a href="$url">$column->{'title'}$arrow</a></div>
				</th>
!;
		}

		$style = "";

		if ( defined $column->{'align'} ) {
			$style .= "text-align: $column->{'align'};";
		}

		if ( defined $column->{'break'} ) {
			push @breaks, $column->{'column'};
		}
		elsif ( defined $column->{'urllimit'} ) {
			push @urls,  $column->{'column'};
		}
		elsif ( defined $column->{'colour'} ) {
			$colourcolumn = $column->{'column'};
			$colourtranslations = $column->{'tr'};
		}
		else {
			# In case no column has been specified, assume column 0.
			if ( not defined $column->{'column'} ) {
				push @columns, "0,$column->{'mark'}";
			}
			elsif ( defined $column->{'mark'} ) {
				push @columns, "$column->{'column'},$column->{'mark'}";
			}
			else {
				push @columns, $column->{'column'};
			}
		}
		push @styles, $style;
		push @translations, $column->{'tr'};
	}
	
	print qq{
		</tr>
	};

	# now we can render the content

	my $colour = "background-color: $table2colour;";
	$i = 0;
	my @lines;

	if (ref($filename) eq "ARRAY") {
		foreach $line (@$filename) {
			my @cols = ( $position++, (split / /, $line) );
			push @lines, \@cols;
		}
	}
	elsif ( open my $input, "$filename" ) {
		my $position = 1;
		while( my $line = <$input> ) {
			chomp $line;
			my @cols = ( $position++, (split /,/, $line) );
			# FFC: change dashes to commas
			if ($cols[4] =~ /-/) {
				$cols[4] =~ s/-/,/g;
			}
			push @lines, \@cols;
		}
		close $input;
	}
	else {
		print "</table>\n";
		return;
	}

	# sort the lines according to the relevant selected row.
	my @sorted_lines;

	if ( ref $sort ) {
		# an overridden sort function.
		if ( $order eq $tr{'log ascending'} ) {
			@sorted_lines = sort { &{$sort}( $a->[$columns[$selected_column-1]], $b->[$columns[$selected_column-1]] ) } @lines;
		}
		else {
			@sorted_lines = sort { &{$sort}( $b->[$columns[$selected_column-1]], $a->[$columns[$selected_column-1]] ) } @lines;
		}
	}
	elsif ( $sort eq "<=>" ) {
		if ( $order eq $tr{'log ascending'} ) {
			@sorted_lines = sort { $a->[$columns[$selected_column-1]] <=> $b->[$columns[$selected_column-1]] } @lines;
		}
		else {
			@sorted_lines = sort { $b->[$columns[$selected_column-1]] <=> $a->[$columns[$selected_column-1]] } @lines;
		}
	}
	else {
		if ( $order eq $tr{'log ascending'} ) {
			@sorted_lines = sort { $a->[$columns[$selected_column-1]] cmp $b->[$columns[$selected_column-1]] } @lines;
		}
		else {
			@sorted_lines = sort { $b->[$columns[$selected_column-1]] cmp $a->[$columns[$selected_column-1]] } @lines;
		}	
	}

	# slice the information up at all ?
	my $sliced = 0;

	if ( defined $settings->{'slice'} and ref $settings->{'slice'} ) {
		my $start = $settings->{'slice'}->{'start'};
		my $end   = $settings->{'slice'}->{'end'};
		$sliced   = scalar @sorted_lines;
		my @slice = splice( @sorted_lines, $start, $end);
		@sorted_lines = @slice;
	}

	foreach my $line (@sorted_lines) {
		my @cols = @{$line};
		print "<tr class='list'>\n";
		my $entry = 0;
		my $rowspan = "";
		# Each comment increments $rowSpanCount
		$rowSpanCount = 1;
		foreach my $reference ( @breaks ) {
			if ( defined $cols[$reference] and $cols[$reference] ne "" ) {
				$rowSpanCount++;
			}
		}
		if ($headerrowspan == 1 and $rowSpanCount > 1) {
			my $rowspan = " rowspan='$rowSpanCount'";
		}
		foreach my $reference ( @columns ) {
			unless ( $reference =~ /,/ ) {
			# are we supposed to translate this at all ?
				my $text = $cols[$reference];
				# If it begins with !, change its color (FFC?)
				if ($cols[$reference] =~ /^\!/) {
					$text = "<font color=#2B60DE>$text</font>";
				}

				if ( defined $translations[$entry] ) {
					my $type = ref $translations[$entry];
					if ( not $type ) {
						if ( $translations[$entry] eq "onoff" ) {
							if ( $cols[$reference] eq "on" ) {
								$text = "<img alt='on' src='/ui/img/on.gif'>";
							}
							else {
								$text = "<img alt='off' src='/ui/img/off.gif'>";
							}
						}
						if ( $translations[$entry] =~ /url/ ) {
							my ($kwd, $charlimit) = split (/:/, $translations[$entry]);
							my $url = $text;
							my $part = substr($text, 0, 80);
							$part .= "..." unless length($part) < 80;
							$text = "<a href='$url' title='$url' target='_new'>";
							$text .= "$part</a>";
						}
					}
					elsif ( $type eq "HASH" and defined $translations[$entry]->{$cols[$reference]} ) {
						$text = $translations[$entry]->{$cols[$reference]};
					}
					elsif ( $type eq "ARRAY" and defined $translations[$entry]->[$cols[$reference]] ) {
						$text = $translations[$entry]->[$cols[$reference]];
					}
				}
				if ( $colourcolumn != 0 ) {
					$text = "<span class='$colourtranslations->{$cols[$colourcolumn]}'>$text</span>";
				}
				print "<td$rowspan class='list' style='$colour $styles[$entry]; padding:.1em .5em'><p style='margin:0'>$text</p></td>\n";
				# Single use!
				$rowspan = "";

			}
			else {
				# this is a "mark" field, i.e. a checkbox
				my $text;
				my ($column, $mark) = split( /,/, $reference );
				my $newmark = "";
				if ( $mark ne " " ) {
					$newmark = $mark;
				}
				# FFC: disable the checkbox when needed
				if ($cols[1] =~ /:/ or !($cols[3] =~ /^eth/ or $cols[3] =~ /^ppp/)) { 
					$text = '';
				}
				else {
					$text = 'DISABLED';
				}
				print "<td class='list' style='$colour $styles[$entry]' onclick=\"toggle_mark('R${id}_$cols[0]');\"><input id ='R${id}_$cols[$column]' type='checkbox' name='$newmark$cols[$column]' onclick=\"toggle_mark('R${id}_$cols[0]');\"></td>";
			}
			$entry++;
		}

		# do we need to render any comments etc ?
		foreach my $reference ( @breaks ) {
			if ( defined $cols[$reference] and $cols[$reference] ne "" ) {
				# FFC/TOFC: delete the leading +
				if ($cols[$reference] =~ /\+/) {
					$cols[$reference] =~ s/\+//;
				}
				print "</tr><tr class='list'><td style='padding:.1em .5em; $colour $styles[$entry]' class='listcomment' colspan='$colcount'><i>$cols[$reference]</i></td>\n";
			}
		}

		$i++;
		print "</tr>\n";
		if ( $colour eq "background-color: $table1colour;" ) {
			$colour = "background-color: $table2colour;";
		} 
		else {
			$colour = "background-color: $table1colour;";
		}
	}
	

	# and end the table
	print qq{
		</table>
};

}

sub ipcompare
{
	my ( $a, $b, $direction ) = @_;

	$direction = 1 if ( $direction != -1 );

	my ( $ipa, $ipb );

	$ipa = $_ + $ipa * 256 for split(/\./, $a);
	$ipb = $_ + $ipb * 256 for split(/\./, $b);

	if ( $direction == 1 ) {
		return ( $ipa <=> $ipb );
	}
	else {
		return ( $ipb <=> $ipa );
	}
}

sub jsvalidip
{
	my ( $id, $blank ) = @_;
	$blank = 'false' if ( not defined $blank or $blank ne "true" );
	my $ret = &script("validip('$id','$blank')");
	push @_validation_items, "validip('$id','$blank')" ;
	return $ret;
}

sub jsvalidmask
{
	my ( $id, $blank ) = @_;
	$blank = 'false' if ( not defined $blank or $blank ne "true" );
	my $ret = &script("validmask('$id','$blank')");
	push @_validation_items, "validmask('$id','$blank')" ;
	return $ret;
}

sub jsvalidipormask
{
	my ( $id, $blank ) = @_;
	$blank = 'false' if ( not defined $blank or $blank ne "true" );
	my $ret = &script("validipormask('$id','$blank')");
	push @_validation_items, "validipormask('$id','$blank')" ;
	return $ret;
}

sub jsvalidipandmask
{
	my ( $id, $blank ) = @_;
	$blank = 'false' if ( not defined $blank or $blank ne "true" );
	my $ret = &script("validipandmask('$id','$blank')");
	push @_validation_items, "validipandmask('$id','$blank')" ;
	return $ret;
}

sub jsvalidport
{
	my ( $id, $blank ) = @_;
	$blank = 'false' if ( not defined $blank or $blank ne "true" );
	my $ret = &script("validport('$id','$blank')");
	push @_validation_items, "validport('$id','$blank')" ;
	return $ret;
}

sub jsvalidportrange
{
	my ( $id, $blank ) = @_;
	$blank = 'false' if ( not defined $blank or $blank ne "true" );
	my $ret = &script("validportrange('$id','$blank')");
	push @_validation_items, "validportrange('$id','$blank')" ;
	return $ret;
}

sub jsvalidmac
{
	my ( $id, $blank ) = @_;
	$blank = 'false' if ( not defined $blank or $blank ne "true" );
	my $ret = &script("validmac('$id','$blank')");
	push @_validation_items, "validmac('$id','$blank')" ;
	return $ret;
}

sub jsvalidcomment
{
	my ( $id, $blank ) = @_;
	$blank = 'false' if ( not defined $blank or $blank ne "true" );
	my $ret = &script("validcomment('$id','$blank')");
	push @_validation_items, "validcomment('$id','$blank')";
	return $ret;
}

sub jsvalidhostname
{
	my ( $id, $blank ) = @_;
	$blank = 'false' if ( not defined $blank or $blank ne "true" );
	my $ret = &script("validhostname('$id','$blank')");
	push @_validation_items, "validhostname('$id','$blank')" ;
	return $ret;
}

sub jsvalidregex
{
	my ( $id, $expr, $blank ) = @_;
	$blank = 'false' if ( not defined $blank or $blank ne "true" );
	my $ret = &script("validregex('$id','$expr', $blank)");
	push @_validation_items, "validregex('$id','$expr',$blank)" ;
	return $ret;
}

sub jsvalidpassword
{
	my ( $id, $id2, $expr, $blank ) = @_;
	$blank = 'false' if ( not defined $blank or $blank ne "true" );
	my $ret = &script("validpassword('$id', '$id2', '$expr', $blank)");
	push @_validation_items, "validpassword('$id', '$id2','$expr',$blank)" ;
	return $ret;
}


sub jsvalidnumber
{
	my ( $id, $min, $max, $blank ) = @_;
	$blank = 'false' if ( not defined $blank or $blank ne "true" );
	my $ret = &script("validnumber('$id', $min, $max, $blank)");
	push @_validation_items, "validnumber('$id', $min, $max, '$blank')" ;
	return $ret;
}








1;

