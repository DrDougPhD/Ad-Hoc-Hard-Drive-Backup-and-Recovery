#!/usr/bin/perl
use strict;
use warnings;

use feature 'say';
use autodie; # die if problem reading or writing a file
use Getopt::Long qw(GetOptions);


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
	say $row;
}


# openr() returns an IO::File object to read from
#my $file_handle = $file->openr();

# Read in line at a time
#while( my $line = $file_handle->getline() ) {
#        print $line;
#}
