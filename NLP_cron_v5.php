
<?php

require 'admin/config.php';
require 'app_tokens_gwTech.php';
// Create an OAuth connection
require 'tmhOAuth.php';

$connection = new tmhOAuth(array(
  'consumer_key'    => $consumer_key,
  'consumer_secret' => $consumer_secret,
  'user_token'      => $user_token,
  'user_secret'     => $user_secret,
  'curl_ssl_verifypeer'   => false
));

$search_terms = array('%40grewpworkTech');

$db = mysqli_connect($dbConfig['host'],$dbConfig['user'],$dbConfig['pass'],$dbConfig['database']);
if (!$db) {
    die('Could not connect: ' . mysql_error());
}

//set_time_limit(60*5);
//for ($i = 0; $i < 9; $i++) {
//$t = microtime(true);
    
////////////////////////////////// **************************   
// code in here


//search for grewpworkTech mentions
foreach ($search_terms as $search) {

//query the newest tweet we have
//$query = "SELECT tweet_id FROM tweet_mentions WHERE target_screen_name = '$search' ORDER BY tweet_id DESC LIMIT 1";
//$result = mysqli_query($db,$query);
//old way
$result = $db->query("SELECT tweet_id FROM tweet_mentions ORDER BY tweet_id DESC LIMIT 1");
//echo "SELECT tweet_id FROM tweet_mentions WHERE target_screen_name = '$search' ORDER BY tweet_id DESC LIMIT 1"."\n";


$row = mysqli_fetch_assoc($result);
$since_id = $row['tweet_id'];
//$since_id = 1;
//echo $since_id;
//echo "<br>";
if(isset($since_id)) {
    
//echo 'test';
//query the oldest tweet we have
//$result = $db->query('SELECT tweet_id FROM tweet_mentions ORDER BY tweet_id LIMIT 1');
//$row = mysqli_fetch_assoc($result);
//$max_id = $row['tweet_id']-1;

// Request the most recent 100 matching tweets
$http_code = $connection->request('GET',$connection->url('1.1/search/tweets'), 
		array(
			'q' => $search,
			'since_id' => $since_id,
			'count' => 5
			
		));

// Search was successful
if ($http_code == 200) {
		
	// Extract the tweets from the API response
	$response = json_decode($connection->response['response'],true);
	$tweet_data = $response['statuses'];
	//print_r($response);
	//echo "<br>";
	//print_r($tweet_data);
	//echo "<br>";
	foreach($tweet_data as $tweet) {
            
            // Ignore any retweets
            if (!isset($tweet['retweeted_status'])) {
		
			
		
		//$tweet_id = $tweet['id'];
		$screen_name = mysqli_real_escape_string($db,$tweet['user']['screen_name']);
		$name = mysqli_real_escape_string($db,$tweet['user']['name']);		
		$profile_image_url = mysqli_real_escape_string($db,$tweet['user']['profile_image_url']);
		$tweet_id = mysqli_real_escape_string($db,$tweet['id_str']);
		$tweet_text = mysqli_real_escape_string($db,$tweet['text']);
		$created_at = mysqli_real_escape_string($db,$tweet['created_at']);
		$created_at = strtotime($created_at);
		$date_collected = time();
		
		$target_screen_name = $search;
                
                // process the request
		$s = str_replace('@grewpworkTech ','',$tweet_text);
		//echo $s."<br>";
		
                //$temp = explode("@grewpworkTech ",$tweet_text);
                //$city = $temp[1];
         
                if(isset($s))
                {
                    $query = 'INSERT INTO '.$tweets.' ('.$user_tweets.') VALUES ("'.$s.'")';
		    mysqli_query($db,$query);
		    
		    $reply = '';
		    //system("/var/chroot/home/content/13/10555713/html/movie/nlp/movie_extraction.py 2>&1", $output);
		    $pid = popen("/var/chroot/home/content/13/10555713/html/movie/nlp2/movie_extraction.py","r");
		    while( !feof( $pid ) )
		    {
			$reply .= fread($pid, 256);
		    }
		    pclose($pid);
		    echo $reply;
		    
		    //check if there is a product to offer
		    if($reply == 'none') {
			if($screen_name != 'grewpworkTech') {
			    $gwTweet = '@'.$screen_name.' Sorry, there are no products that match your request #MIEmoviebot id:'.$tweet_id;
                            // Send a tweet
                            $code = $connection->request('POST', 
                                    $connection->url('1.1/statuses/update'), 
                                    array('status' => $gwTweet));
			    if($code != 200){
				$gwTweet = '@'.$screen_name.' error code:'.$code.' id:'.$tweet_id;
				$code = $connection->request('POST', 
                                    $connection->url('1.1/statuses/update'), 
                                    array('status' => $gwTweet));
			    }
			}
		    }
		    //there is a response id
		    else {
			if($screen_name != 'grewpworkTech') {
			    $gwTweet = '@'.$screen_name.' Click on http://grewpwork.com/movie/reply.html?'.$reply.' #MIEmoviebot';
                            // Send a tweet
                            $code = $connection->request('POST', 
                                    $connection->url('1.1/statuses/update'), 
                                    array('status' => $gwTweet));
			    if($code != 200){
				$gwTweet = '@'.$screen_name.' error code:'.$code.' id:'.$tweet_id;
				$code = $connection->request('POST', 
                                    $connection->url('1.1/statuses/update'), 
                                    array('status' => $gwTweet));
			    }
			}
		    }
		 
		 
		 
		    //echo $s."<br>";
		    //echo $movie."<br>";
		    /*
		    $querys = 'UPDATE '.$tweets.' SET '.$user_tweets.'="'.$s.'", '.$user_response.'="'.$movie.'" WHERE '.$user_tweets.'="'.$s.'"';
		    //$querys = "UPDATE ".$tweets." SET ".$user_tweets."='".$s."', ".$user_response."='".$movie."' WHERE ".$user_tweets."='".$s."'";
		    mysqli_query($db,$querys);
		    */
		    
                    
                    
                    
                } // end if $s
		
		//input tweet
		$query = "
			INSERT into tweet_mentions
			set 	tweet_id = '".$tweet_id."',
				created_at = ".$created_at.",
				source_screen_name = '".$screen_name."',
				target_screen_name = '".$target_screen_name."',
				tweet_text = '".$tweet_text."'";
			
		$db->query($query); 
		
		//check if user exists
		$query = "
			SELECT name
			FROM screen_names
			where screen_name = '".$screen_name."'
		";
		$result = $db->query($query); 
		if($result->num_rows == 0) {
			//insert user
			$query = "
			INSERT into screen_names
			set 	screen_name = '".$screen_name."',
				name = '".$name."',
				profile_image_url = '".$profile_image_url."',
				date_collected = ".$date_collected;
			
			$db->query($query);
		}
	
                
            }// end if reTweet
        }//end of for each tweet loop
// Handle errors from API request
} // end if http_code == 200

else {
	if ($http_code == 429) {
	    $to = 'k.ferreira.mie@gmail.com';
	    $subj = 'code error 429';
	    $body = 'Error: Twitter API rate limit reached';
	    mail($to,$subj,$body);
	}
	else {
	    $to = 'k.ferreira.mie@gmail.com';
	    $subj = 'code error: '.$http_code;
	    $body = 'Error: Twitter was not able to process';
	    //mail($to,$subj,$body);
	    //echo $subj."<br>";
	}
    
} // end else http code == 200

}// end of if since id is set
}//end of foreach search term	

    
    
////////////////////////////////// **************************

//sleep(30);

//} // end of time loop
//echo 'DONE';

$db->close();


?>