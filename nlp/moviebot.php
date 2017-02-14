<?php
require 'tmhOAuth.php';
require 'tmhUtilities.php';
require 'login.php';
require 'app_tokens.php';
require 'create_database.php';

define ("COUNT", 1);

$tmhOAuth = new tmhOAuth(array(
  'consumer_key' => $consumer_key,
  'consumer_secret' => $consumer_secret,
  'user_token' => $user_token,
  'user_secret' => $user_secret,
  'curl_ssl_verifypeer'   => false
));

// Connect to mysql
$connection = mysqli_connect("$host", "$username", "$password");
if(mysqli_connect_errno())
{
	echo "Failed to connect to MySQL: " . mysqli_connect_error();
}
else
{
	echo 'Connection OK'."<br>";
}

// Setup database and tables
for ($i = 0; $i < sizeof($sql); $i++){
	mysqli_query($connection,$sql[$i]);
	$connection = mysqli_connect("$host", "$username", "$password", "$database");
}

$code = $tmhOAuth->request('GET', $tmhOAuth->url('1.1/statuses/mentions_timeline'), array('count' => COUNT, 'contributor_details' => "true"));

$response = $tmhOAuth->response['response'];
$twitFeed = json_decode($response, true);   

for ($i = 0; $i < COUNT; $i++){
	if (isset($twitFeed[$i])){
		$screenNameOfContributor = $twitFeed[$i]['user']['screen_name'];
		$feedMsg = $twitFeed[$i]['text'];

		$s = str_replace('@MIEMovieBot ','',$feedMsg);
		$query = "INSERT INTO ".$tweets." (".$user_tweets.", ".$user_response.") VALUES ('".$s."', '')";
		mysqli_query($connection,$query);

		system('nlp\movie_extraction.py');

		//$querys = "SELECT ".$user_response." FROM ".$tweets." ORDER BY ".$id." DESC LIMIT 1";
		$querys = "SELECT user_response from tweets ORDER by id DESC LIMIT 1";
		$result = mysqli_query($connection,$querys);
		$response = mysqli_fetch_row($result);
		echo $response[0];
		//$code = $tmhOAuth->request('POST', $tmhOAuth->url('1.1/statuses/update'), array('status'=>"@".$screenNameOfContributor.' '.$what));

		//if ($code == 200){
		//	echo "Tweet Sent";
		//}
		//else{
		//echo "Error: $code";
		//}
	}
	else{
		echo "SOME ERROR";
	}


}
?>