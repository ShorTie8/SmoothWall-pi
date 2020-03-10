package Stans::modlib;

our @EXPORT = qw();

our @EXPORT_OK = qw(
		   ifcolormap
		   portsmap
		   protocolmap
		   dispaliastab2
		 );

our %EXPORT_TAGS = ( standard => [@EXPORT_OK], );

our $VERSION = '1.0';

sub ifcolormap
{
	my (%ifcolors, $line, $ifcolor, $ethdev, $ethcolor);
	
	open(FILE, "/var/smoothwall/mods/fullfirewall/portfw/aliases") or die 'Unable to open';
	while ( $line = <FILE> ){
		chomp $line;
		next if ( $line eq "" );
	
		( $ifcolor, $ethdev ) = split /,/, $line;
		if ($ifcolor =~ /^RED/) {
			$ethcolor = "<font color=red>$ifcolor</font>";
		} elsif ($ifcolor =~ /^GREEN/) {
			$ethcolor = "<font color=green>$ifcolor</font>";
		} elsif ($ifcolor =~ /^ORANGE/) {
			$ethcolor = "<font color=orange>$ifcolor</font>";
		} elsif ($ifcolor =~ /^PURPLE/) {
			$ethcolor = "<font color=purple>$ifcolor</font>";
		} else {
			$ethcolor = $ifcolor;
		}
		$ifcolors{$ethdev} = "$ethcolor ($ethdev)";
	}
	close FILE;
	return \%ifcolors;
}

sub portsmap
{
	my %ports;
	my $portfiles = "/var/smoothwall/knownports/*";
	
	foreach my $filenames ( glob $portfiles ){
		unless (open(FILE, $filenames))
		{
			next;
		}

		while ( my $line = <FILE> ){
			chomp $line;
			next if ( $line eq "" );
	
			my ( $name, $value ) = split /,/, $line;

			if ($value eq "0") {
				$ports{$value} = '*';
			} else {
				$ports{$value} = "$name ($value)";
			}
		}
	}
	return \%ports;
}

sub protocolmap
{
	my %protocollist;
	
	open(FILE, "/var/smoothwall/mods/fullfirewall/portfw/protolist") or die 'Unable to open protocol list file';
	while ( my $line = <FILE> ){
		chomp $line;
		next if ( $line eq "" );

		my ($protocoln, $proto) = split /,/, $line;	
		$protocollist{$protocoln} = $proto;
	}
	close FILE;
	return \%protocollist;
}

sub dispaliastab2
{
  my ( $filename, $settings, $order, $selected_column, $id ) = @_;

  # 'id' can be used to give us a different name, *iff* we are repeating the
  # widget.	

  print qq{
    <table class='list' style='margin:6pt 0'>
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

  my ( $table1colour, $table2colour ) = ( '#f0f0f0', '#e0e0e0' );

  foreach my $column ( @{$settings->{'columns'}} ){
    my $span = "";
    my $style = "background-color: $table2colour;";
    my $class = "list";

    if ( defined $column->{'maxrowspan'} ) {
      $rowspan = " rowspan='$column->{'maxrowspan'}'";
    } else {
      $rowspan = "";
    }

    if ( defined $column->{'rotate'} ) {
      $rotate = "; transform:rotate($column->{'rotate'}deg);";
      if ( defined $column->{'valign'} ) {
        $style .= "vertical-align:middle;";
      }
    } else {
      $rotate = "";
      if ( defined $column->{'valign'} ) {
        $style .= "vertical-align:bottom;";
      }
    }

    if ( defined $column->{'align'} ){
      $style .= "text-align: $column->{'align'};";
    }

    if ( defined $column->{'break'} ){
      print "</tr><tr>";
      $colcount = scalar(@columns) + $column->{'spanadj'};
      $span = " colspan='$colcount'";
      $class = "list";
    } else {
      $style .= "border-bottom:1px solid #b0b0b0;";
    }

    if ( $rotate eq "" ){
      if ( defined $column->{'size'} ){
        $style .= "width: $column->{'size'}%;";
      }
    } else {
      $style .= "width:.01%; height:6em;";
    }

    my $arrow;
    my $url = $settings->{'url'};
    $i++;
    $url =~s/\[%COL%\]/$i/;		

    if ( $i == $selected_column ){
      if ( $order eq $tr{'log ascending'} ){
        $url =~s/\[%ORD%\]/$tr{'log descending'}/;
        $arrow = "&nbsp;<img src='/ui/img/down.jpg' alt='change direction'>";
      } else {
        $url =~s/\[%ORD%\]/$tr{'log ascending'}/;
        $arrow = "&nbsp;<img src='/ui/img/up.jpg' alt='change direction'>";
      }

      # choose a sorting algorithm
      if ( defined $column->{'sort'} ){
        $sort = $column->{'sort'};
      }

    } else {
      $url =~s/\[%ORD%\]/$tr{'log ascending'}/;
    }

    if ( not defined $column->{'colour'} ){
      print qq !
        <th$span$rowspan class='$class' style='$style; padding:.05em .5em'>
          <div style="a$rotate"><a href="$url">$column->{'title'}$arrow</a></div>
        </th>
!;
    }

    $style = "";
    if ( defined $column->{'align'} ){
      $style .= "text-align: $column->{'align'};";
    }


    if ( defined $column->{'break'} ){
      push @breaks, $column->{'column'};
    } elsif ( defined $column->{'urllimit'} ){
      push @urls,  $column->{'column'};
    } elsif ( defined $column->{'colour'} ){
      $colourcolumn = $column->{'column'};
      $colourtranslations = $column->{'tr'};
    } else {
      # In case no column has been specified, assume column 0.
      if ( not defined $column->{'column'} ){
        push @columns, "0,$column->{'mark'}";
      } elsif ( defined $column->{'mark'} ){
        push @columns, "$column->{'column'},$column->{'mark'}";
      } else {
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

  my $colour = "background-color: $table1colour;";
  $i = 0;
  my @lines;

  if (ref($filename) eq "ARRAY"){
    foreach $line (@$filename) {
      my @cols = ( $position++, (split / /, $line) );
      push @lines, \@cols;
    }
  } elsif ( open my $input, "$filename" ){
    my $position = 1;
    while( my $line = <$input> ){
      chomp $line;
      my @cols = ( $position++, (split /,/, $line) );
      if ($cols[4] =~ /-/) {
        $cols[4] =~ s/-/,/g;
      }
      push @lines, \@cols;
    }
    close $input;
  } else {
    print "</table>\n";
    return;
  }

  
  # sort the lines according to the relevant selected row.
  my @sorted_lines;

  if ( ref $sort ){
    # an overridden sort function.
    if ( $order eq $tr{'log ascending'} ){
      @sorted_lines = sort { &{$sort}( $a->[$columns[$selected_column-1]], $b->[$columns[$selected_column-1]] ) } @lines;
    } else {
      @sorted_lines = sort { &{$sort}( $b->[$columns[$selected_column-1]], $a->[$columns[$selected_column-1]] ) } @lines;
    }
  } elsif ( $sort eq "<=>" ){
    if ( $order eq $tr{'log ascending'} ){
      @sorted_lines = sort { $a->[$columns[$selected_column-1]] <=> $b->[$columns[$selected_column-1]] } @lines;
    } else {
      @sorted_lines = sort { $b->[$columns[$selected_column-1]] <=> $a->[$columns[$selected_column-1]] } @lines;
    }
  } else {
    if ( $order eq $tr{'log ascending'} ){
      @sorted_lines = sort { $a->[$columns[$selected_column-1]] cmp $b->[$columns[$selected_column-1]] } @lines;
    } else {
      @sorted_lines = sort { $b->[$columns[$selected_column-1]] cmp $a->[$columns[$selected_column-1]] } @lines;
    }	
  }

  # slice the information up at all ?
  my $sliced = 0;

  if ( defined $settings->{'slice'} and ref $settings->{'slice'} ){
    my $start = $settings->{'slice'}->{'start'};
    my $end   = $settings->{'slice'}->{'end'};
    $sliced   = scalar @sorted_lines;
    my @slice = splice( @sorted_lines, $start, $end);
    @sorted_lines = @slice;
  }

  foreach my $line (@sorted_lines){
    my @cols = @{$line};
    print "<tr class='list'>\n";
    my $entry = 0;
    # Each comment increments $rowSpanCount
    $rowSpanCount = 1;
    foreach my $reference ( @breaks ){
      if ( defined $cols[$reference] and $cols[$reference] ne "" ){
        $rowSpanCount++;
      }
    }
    my $rowspan = " rowspan='$rowSpanCount'";
    foreach my $reference ( @columns ){
      unless ( $reference =~ /,/ ){
      # are we supposed to translate this at all ?
        my $text = $cols[$reference];
        if ($cols[$reference] =~ /^\!/) {
          $text = "<font color=#2B60DE>$text</font>";
        }

        if ( defined $translations[$entry] ){
          my $type = ref $translations[$entry];
          if ( not $type ) {
            if ( $translations[$entry] eq "onoff" ){
              if ( $cols[$reference] eq "on" ){
                $text = "<img alt='on' src='/ui/img/on.gif'>";
              } else {
                $text = "<img alt='off' src='/ui/img/off.gif'>";
              }
            }
            if ( $translations[$entry] =~ /url/ ){
              my ($kwd, $charlimit) = split (/:/, $translations[$entry]);
	      my $url = $text;
	      my $part = substr($text, 0, 80);
	      $part .= "..." unless length($part) < 80;
              $text = "<a href='$url' title='$url' target='_new'>";
	      $text .= "$part</a>";
            }
          } elsif ( $type eq "HASH" and defined $translations[$entry]->{$cols[$reference]} ){
            $text = $translations[$entry]->{$cols[$reference]};
          } elsif ( $type eq "ARRAY" and defined $translations[$entry]->[$cols[$reference]] ){
            $text = $translations[$entry]->[$cols[$reference]];
          }
        }
        if ( $colourcolumn != 0 ){
          $text = "<span class='$colourtranslations->{$cols[$colourcolumn]}'>$text</span>";
        }
        print "<td$rowspan class='list' style='$colour$styles[$entry]; padding:.1em .5em' onclick=\"toggle_row('${id}_$cols[0]');\" ><p style='margin:0'>$text</p</td>\n";
        # Single use!
        $rowspan = "";

      } else {
        # this is a "mark" field, i.e. a checkbox
        my $text;
        my ($column, $mark) = split( /,/, $reference );
        my $newmark = "";
        if ( $mark ne " " ){
          $newmark = $mark;
        }
        if ($cols[1] =~ /:/ or !($cols[3] =~ /^eth/ or $cols[3] =~ /^ppp/)) { 
          $text = '';
        } else {
          $text = 'DISABLED';
        }
        print "<td class='list' style='$colour$styles[$entry]'><input id ='${id}_$cols[$column]' type='checkbox' name='$newmark$cols[$column]' $text></td>";
      }
      $entry++;
    }

    # do we need to render any comments etc ?
    foreach my $reference ( @breaks ){
      if ( defined $cols[$reference] and $cols[$reference] ne "" ){
        if ($cols[$reference] =~ /\+/) {
          $cols[$reference] =~ s/\+//;
        }
        print "</tr><tr class='list'><td style='padding:.1em .5em; $colour$styles[$entry]' class='listcomment' colspan='$colcount'$styles[$entry]><i>$cols[$reference]</i></td>\n";
      }
    }

    $i++;
    print "</tr>\n";
    if ( $colour eq "background-color: $table1colour;" ){
      $colour = "background-color: $table2colour;";
    } else {
      $colour = "background-color: $table1colour;";
    }
  }
  

  # and end the table
  print qq{
    </table>
  };

}





1;


__END__
# Below is stub documentation for your module. You'd better edit it!

=head1 NAME

Stans::modlib - Perl extension for blah blah blah

=head1 SYNOPSIS

  use Stans::modlib;

=head1 DESCRIPTION

A collection of subs for use with the Full Firewall Control mod for SWE.

=head2 EXPORT

None by default.



=head1 SEE ALSO

None: Personal perl module

=head1 AUTHOR

Stanford Prescott, E<lt>sprescott58@comcast.netE<gt>

=head1 COPYRIGHT AND LICENSE

Copyright (C) 2011 by Stanford Prescott

This library is free software; you can redistribute it and/or modify
it under the same terms as Perl itself, either Perl version 5.8.8 or,
at your option, any later version of Perl 5 you may have available.


=cut
