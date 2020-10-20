#!/usr/bin/perl -T -w
use strict;
use warnings;
use Fcntl qw(:flock);
use CGI;
my $q = new CGI;
use URI::Escape;



my $success = "true";
my $id = 0;
my $debug = "";

# verify that the experiment name is there
if(!$q->url_param("experimentName") || $q->url_param("experimentName")!~/^[A-Za-z0-9]+$/) {
	$success = "false";
}

my $sourceurl = uri_escape($q->url_param("sourceurl"),"^A-Za-z0-9\.\%\~\!\*\(\)\'");
if(!$sourceurl || $sourceurl!~/^[A-Za-z0-9\.\%\~\!\*\(\)\']+$/) {
	$success = "false";
}

if ($success eq "true") {

	# un-tainting the experiment name
	my $exp = $q->url_param("experimentName");
	$exp =~ /^([A-Za-z0-9]+)$/;
	my  $experimentName = $1;

	# un-tainting the source url
	$sourceurl =~ /^([A-Za-z0-9\.\%\~\!\*\(\)\']+)$/;
	my $sourceURL = $1;
	
	# simplifying the source URL
	$sourceURL =~ s/^http%3A%2F%2F//;
	$sourceURL =~ s/%2F$//;
	$sourceURL =~ s/%3A/./g;
	$sourceURL =~ s/%2F/./g;
	$sourceURL =~ s/%7E//g;
	$sourceURL =~ s/~//g;


	####can't use without the appropriate module
	####make_path("storage"."/".$sourceURL."/".$experimentName);

	# create a folder for the experiment if it isn't there
	if (-d "storage/".$sourceURL."/".$experimentName) {
		# folder exists, nothing to do
	}
	else {
		# make folder
		mkdir "storage/".$sourceURL , 0777;
		mkdir "storage/".$sourceURL."/".$experimentName, 0777;
	}

	# find userfile with biggest number, add one
	opendir(USERS,"storage"."/".$sourceURL."/".$experimentName) or die "Couldn't open user directory $!";
	while (my $file = readdir(USERS)) {
		if ($file =~ /^user(\d+).txt$/) {
			$id = $1 if $1>$id;
		}
	}
	closedir(USERS) or die "Couldn't close user directory $!";
	$id++;


	
# 	if (-d "storage"."/".$sourceURL."/".$experimentName) {
# 		# directoy exists, find last user
# 		opendir(USERS,"storage"."/".$sourceURL."/".$experimentName) or die "Couldn't open user directory $!";
# 		while (my $file = readdir(USERS)) {
# 			if ($file =~ /^user(\d+).txt$/) {
# 				$id = $1 if $1>$id;
# 			}
# 		}
# 		closedir(USERS) or die "Couldn't close user directory $!";
# 		$id++;
# 	}
# 	else {
# 		# create directory
# 		make_path("storage"."/".$sourceURL."/".$experimentName);
# 	}





}

my $callback = $q->url_param("callback") || "";
my $str = '"' . $id . '"';

print $q->header(-charset=>'utf-8');
print $callback . '(' . $str . ')' ;



