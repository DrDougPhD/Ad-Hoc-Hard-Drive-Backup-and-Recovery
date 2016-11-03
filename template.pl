#!/usr/bin/perl
use strict;
use warnings;

use feature 'say';
use autodie; # die if problem reading or writing a file
use Getopt::Long qw(GetOptions);
use File::Basename qw(basename);
use Digest::MD5;


my $files_in_dir = "/media/kp/bde47223-0184-4d33-a224-c3622c62920c/Backup/jazzpony/";
my $file_list = "/home/kp/Documents/Backup_Review/Jazzpony/sample.txt";
my $dir_to_store_files = './';
GetOptions(
	'within=s'	=> \$files_in_dir,
	'from=s'	=> \$file_list,
	'to=s'		=> \$dir_to_store_files,
) or die "Usage: $0 --within DIRECTORY --from LIST_OF_FILES --to DIRECTORY\n";
 
say $files_in_dir;
say $file_list;
say $dir_to_store_files;
say "-------------------";

open(my $fh, '<:encoding(UTF-8)', $file_list)
	or die "Could not open file '$file_list' $!";

while (my $row = <$fh>) {
	chomp $row;
	my $abs_path = $files_in_dir . $row;
	say "Absolute path: $abs_path";
	if ( -e $abs_path ) {
		# check if this file is linked to in the 'to' directory
		link_file($abs_path, $dir_to_store_files);

	} else {
		say "No file exists: $row";
	}
}


sub link_file {
	my $abs_path = $_[0];
	my $destination_directory = $_[1];

	my $destination = $destination_directory . (basename $abs_path);
	say "Link from: $destination";

	if ( -e $destination ) {
		something($destination, $abs_path);
	} else {
		symlink( $abs_path, $destination );
	}
}


sub something {
	my $old_file = $_[0];
	my $new_file = $_[1];
	open (my $old_fh, '<', $old_file) or die "Can't open '$old_file': $!";
	open (my $new_fh, '<', $new_file) or die "Can't open '$new_file': $!";

	my $checksum = Digest::MD5->new;
	$checksum->addfile($old_fh);
	my $digest=$checksum->hexdigest;
	say "New file checksum: $digest";

	my $cs1 = Digest::MD5->new;
	$cs1->addfile($new_fh);
	my $d1 = $cs1->hexdigest;
	say "New file checksum: $d1";

	if ( $cs1->hexdigest eq $checksum->hexdigest ) {
		say "Unequal checksums. Link new file using checksum.";
	} else {
		say "Checksums are equal! No new file to be linked.";
	}
}


# openr() returns an IO::File object to read from
#my $file_handle = $file->openr();

# Read in line at a time
#while( my $line = $file_handle->getline() ) {
#        print $line;
#}
