# CloudMLAcademy
Hands on Labs practicals files

S3-- Static Website for static files  
Lambda handler for api requests  
DB  for persist     ----  RDS Postgres

![alt text](architecture.jpg)

Step 1) Create S3 bucket named hotel-checkin

    a) Uncheck "Block all public access" to allow public access, acknowledge and create bucket
    b) After creating bucket GOTO bucket permission TAB to to provide permission.
        
        Allow bucket policy anonymous access: 
        ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": [
                        "s3:GetObject"
                    ],
                    "Resource": [
                        "arn:aws:s3:::Bucket-Name/*"
                    ]
                }
            ]
        }
        ```

    c) GOTO bucket properties TAB where enable S3 static website
    d) Upload the html files in this bucket


Step 2) Creating RDS/Postgress DB steps

    a) Create a security group to enable incoming on port 5432 from anywhere. This is required to setup to allow postgres incoming connection.
    b) Create a Postgres Database:
    c) Choose free tier: 
    d) username: postgres 
    e) pwd: Postgres1!
    f) Choose security group which we created in Step a.
    g) Choose Publicly Accessible
    g) In Additional Configuration, disable Automated Backup

Step 3) Check the DB connection.

   a) Connect using dbeaver client from your laptop
   b) Create a database hotel-checkin use namesapce default.
   c) The database will not list, you need to make a new postgressql connection and put hotel-checkin as db.


Step 4) Create table for our application in hotel-checkin DB

    ```sql
    CREATE TABLE checkins (
        id SERIAL PRIMARY KEY,
        guest_name VARCHAR(100) NOT NULL,
        email VARCHAR(150) NOT NULL,
        booking_id VARCHAR(50) NOT NULL,
        room_type VARCHAR(50),
        checkin_date DATE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ```


Step 5) Now create a lambda for savecheckin and list checkins

    a) In AWS console search for Lambda then create Function then Provide below details.
        1) Function name -- save-checkin-lambda
        2) RUntime -- Python 3.12 
        3) Additional Configuration-
            Select default VPC (Attach the lambdas to a vpc because they need to access RDS)
            Select any Subnet 
            Security Group -- Selct default.
        Create Function
    
    b) In the code tab paste the savecheckins.py code
    c) In the Configuration TAB set the below property under environment
        DB_HOST : <RDS DB HOST NAME>
        DB_USER : postgres
        DB_PASS : Postgres1!
    d) In the python file we are using an external module psycopg to make a connection with DB. But that was not supported by AWS. SO make the programme run either you need to create your own layer (where you can create the layer with require module) or use the someone created layer. So will use the existing layer.
        For postgres module --> arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p312-psycopg:20
    e) Under Test TAB paste the below JSON and run
        ```json
        {
            "body": "{\"name\": \"John Doe\", \"email\": \"john.doe@example.com\", \"bookingId\": \"BK123456\", \"roomType\": \"Deluxe Suite\", \"checkinDate\": \"2026-01-16\"}"
        }
        ```

Step 7) Simple Lambda
        a)Create a simple lambda function using file simplePythonLamda
        b) Generate function URL
        c) Enable CORS
        d) Test from postman using the URL and body as:
        {
            "key1": "amit",
            "key2": "nisha",
            "key3": "supriya"
         }

Step 6) Create Lambda function URL for hotel checkin app

        a) Under the Lambda click on Configuration TAB --> Function URL --> Create Function URl
            AUTH Type : NONE
            Additional Settings : 
                Select Check Box --> Configure cross-origin resource sharing (CORS)
                Allow headers --> content-type
                Allow origin --> *
                Allow Method --> *
            Create the Function URL :
        b) It will generate teh below Function URL 
            save-checkin --> https://khgcze5fzy3wposbtr7kbd2loy0rrqfi.lambda-url.us-east-1.on.aws/
                Copy this URL in index.html
            list-checkin --> https://x7bhmyh7qhwnrpx3thousnpscq0ziawn.lambda-url.us-east-1.on.aws/
                Copy this URL in bookings.html

Step 7) Goto bucket and update the URL's for static website and list bookings in the html file

Now open the static website url and make a booking and list bookings.

Step 8) Once all done delete all resources RDS db, Lambda and buckets to avoid billing
