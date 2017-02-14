<?php
    require 'admin/config.php';
    
    
    $method = $_SERVER['REQUEST_METHOD'];
    
    if(strtolower($method) == 'get'){
        
        //$response_id = $_GET['id'];
        //$title = isset($_GET['username']) ? $_GET['username'] : $_POST['username'];
        //$movie_title = 'Godzilla';
        $connect = mysqli_connect($dbConfig['host'], $dbConfig['user'], $dbConfig['pass'],$dbConfig['database']);
        $response_id = mysqli_real_escape_string($connect,$_GET['id']);
               
        if($connect){
            
            //echo 'Hello';
            
            $query1 = "SELECT product_id FROM bi_response WHERE response_id = ".$response_id;
            //echo $query;
            $result1= $connect->query($query1);
            
            if($result1){
            
                
                while($row=$result1->fetch_array(MYSQLI_BOTH))
                {
                    extract($row);
                    $channel[] = array(
                     'product_id' => $product_id
                      
                    );
                }   
                $json = json_encode($channel);
                echo $json;
                
                
                
            }
            
        } else{
            die('Could not connect to MySQL: ' . mysql_error());
        }
    }


?>