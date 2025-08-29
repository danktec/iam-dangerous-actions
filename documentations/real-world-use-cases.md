# Real-world use cases for ```iam-dangerous-actions```: 

Below are some practical, real-world use case scenarios for using ```iam-dangerous-actions```. 


## Scenario 1: Quick "lock-down" of IAM Roles

For the first scenario, we will assume that a **security incident**, or **very strict time constraints** require us to quickly secure specific IAM roles in the AWS account(s). These IAM roles can belong to federated Identity Providers, permission-sets, standlone Identity-based IAM Roles, or AWS Service-roles.

- **Step 1**: 

    Let's begin by attaching the following four explicit-deny IAM policies to the problematic IAM Role(s), based on the following security risks: [PE](https://github.com/ZiyadAlmbasher/iam-dangerous-actions/blob/main/lists/explicit-deny-PE-risk.txt), [DE](https://github.com/ZiyadAlmbasher/iam-dangerous-actions/blob/main/lists/explicit-deny-DE-risk.txt), [DC](https://github.com/ZiyadAlmbasher/iam-dangerous-actions/blob/main/lists/explicit-deny-DC-risk.txt) and [HT](https://github.com/ZiyadAlmbasher/iam-dangerous-actions/blob/main/lists/explicit-deny-HT-risk.txt). This would mitigate the security risks until further steps are taken. 

<br />

- **Step 2**: 

    Finally, we should deploy new SCPs to safeguard these customer-managed, explicit-deny IAM policies against unauthorized access by anyone except security and cloud administrators.

<br />

## Scenario 2: Finding all dangerous IAM Roles in the AWS account

This is a very common use-case: identifying **all existing** IAM Roles that could pose a security threat (contain dangerous IAM actions in them) if abused by malicious users, whether internal or external. The same concept applies to legitimate users who performed damaging operations accidentely. 

- **Step 1**:

  To avoid conflicts with existing installed packages, it is strongly recommended to run this demo in a new Docker container. The steps include everything required to make things work on a base container.

  First, we will install and run [iam-collect](https://github.com/cloud-copilot/iam-collect) in order to retrieve the AWS IAM data locally, as well as [iam-lens](https://github.com/cloud-copilot/iam-lens), which the script in Step 2 below will use. 
  
  We will also install Python, Node, and other necessary packages. 
  
  The demo has been tested and confirmed to work on Ubuntu Linux. For MacOS users, you can use this [script](https://github.com/ZiyadAlmbasher/iam-dangerous-actions/blob/main/scripts/all-actions-for-all-roles-mac.sh) instead. 

  ```bash
  cd ~ && mkdir iam-demo1 && cd iam-demo1  

  sudo apt update
  sudo apt install -y python3 jq git curl unzip  

  ## removing existing apt nodejs versions and installing v22.18.0 through nvm to avoid conflicts: 
  sudo apt purge nodejs npm
  sudo apt autoremove
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
  source ~/.bashrc 
  nvm install v22.18.0
  source ~/.bashrc && npm install -g npm@11.5.2

  ## installing the AWS CLI and aws configure: 
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" 
  unzip awscliv2.zip && cd aws && sudo ./install &&  cd ~/iam-demo1

  aws configure 
    AWS Access Key ID [None]: (press enter to leave empty)
    AWS Secret Access Key [None]: (press enter to leave empty)
    Default region name [None]: us-east-1   
    Default output format [None]: json
  
  export AWS_ACCESS_KEY_ID="your-access-key"
  export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
  export AWS_SESSION_TOKEN="your-session-token"

  npm install -g @cloud-copilot/iam-collect

  iam-collect init
  iam-collect download --services iam

  npm install -g @cloud-copilot/iam-lens
  ```  
<br />

- **Step 2**:

   The next step is to run the following [shell script](https://github.com/ZiyadAlmbasher/iam-dangerous-actions/blob/main/scripts/all-actions-for-all-roles.sh), kindly provided by [David Kerber](https://www.linkedin.com/in/davidkerber/). The script will create one .txt file corresponding to **every single** IAM role in the account. 
   
   Each .txt file will include the sum of all the IAM actions associated with its respective role. All results are stored in a new ```results``` folder:

  ```bash
  cd ~/iam-demo1

  git clone https://github.com/ZiyadAlmbasher/iam-dangerous-actions/
  
  cp iam-dangerous-actions/scripts/all-actions-for-all-roles.sh . 

  sh all-actions-for-all-roles.sh 
  ``` 

  Here is a sample terminal output of ```all-actions-for-roles.sh```: 
  ```bash
  Processed arn:aws:iam::111222333444:role/service-role/ABC -> results/arn_aws_iam__111222333444_role_service-role_ABC.txt
  Processed arn:aws:iam::111222333444:role/DEF -> results/arn_aws_iam__111222333444_role_DEF.txt
 
  All actions for roles have been processed. Check the results directory.
  ```
<br />

 - **Step 3**:

   Lastly, using this AI-generated [python script](https://github.com/ZiyadAlmbasher/iam-dangerous-actions/blob/main/scripts/IAM_cross_checker_MP.py), we can now cross-check any of the available ```iam-dangerous-actions``` [lists](https://github.com/ZiyadAlmbasher/iam-dangerous-actions/tree/main/lists) against the ```results``` folder, which contains all of the IAM Role files, and their respective permissions. For this example, we will use the ```iam-actions-HT-risk.txt``` list. 

   **Side-note:** Using any of the lists with security risks assigned to their IAM actions will save a significant amount of effort later on, compared to choosing the ```dangerous-iam-actions`` with no security risks assigned. This is because **the output** will include the IAM actions and their respective security risks, rather than having to do so manually.
   <br />

   ```bash
   cd ~/iam-demo1
  
   cp iam-dangerous-actions/scripts/IAM_cross_checker_MP.py . && cp iam-dangerous-actions/lists/iam-actions-HT-risk.txt .   
  
   python3 IAM_cross_checker_MP.py iam-actions-HT-risk.txt results output-all-dangerous-roles.txt 
   ```
  
   Sample terminal output of IAM_cross_checker_MP.py: 
   ```
   Loaded 56 actions from iam-actions-HT-risk.txt
   Processing IAM Role: arn_aws_iam__111222333444_role_ABC
   ... ... 
   Processing IAM Role: arn_aws_iam__111222333444_role_DEF
   Report generated: output-all-dangerous-roles.txt
   Roles processed: 125
   Roles with matches: 44
   ```
 
   Sample file output of output-all-dangerous-roles.txt:
   ``` 
   Role: arn_aws_iam__111222333444_role_Beanstalk-EC2-Role
   "s3:PutObject": HT
   --------------------------------------------------
   Role: arn_aws_iam__111222333444_role_Lambda
   "s3:DeleteObject": HT
   "s3:PutObject": HT
   ...  
   ```
   The output file, ```output-all-dangerous-roles.txt```, contains the ```iam-dangerous-actions``` found across all of the IAM Roles in the account. Using one of the ```iam-dangerous-actions-with-security-risks``` lists provides output with IAM actions and their respective security risks. Happy auditing!



<br />

 - **Step 4**:

   Cleaning up iam-demo1: 

    ```bash
    cd ~ && rm -rf ~/iam-demo1
    ```

<br />

## Scenario 3: Checking which IAM policies are "dangerous" 

In Scenario 3, we will check if **newly created** or **existing** IAM policies contain any dangerous IAM actions. We will use an AI-generated [python script](https://github.com/ZiyadAlmbasher/iam-dangerous-actions/blob/main/scripts/IAM_cross_checker_SP.py), which will identify the presence of ```dangerous-iam-actions``` across any IAM policy we would like to audit.  


- **Step 1**: 

    It is strongly recommended to run this demo in a new Docker container, to avoid conflicts with existing installed packages. 


    First, let's gather **all** the customer-managed IAM policies in the account using [iam-collect](https://github.com/cloud-copilot/iam-collect), so they are available locally. We will also ensure that node-js is running above version 20.x: 


    ```bash
    cd ~ && mkdir iam-demo2 && cd iam-demo2  

    sudo apt update
    sudo apt install -y python3 jq git curl unzip  

    ## removing existing apt nodejs versions and installing v22.18.0 through nvm to avoid conflicts: 
    sudo apt purge nodejs npm
    sudo apt autoremove
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
    source ~/.bashrc 
    nvm install v22.18.0
    source ~/.bashrc && npm install -g npm@11.5.2

    ## installing the AWS CLI and aws configure: 
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" 
    unzip awscliv2.zip && cd aws && sudo ./install &&  cd ~/iam-demo2

    aws configure 
      AWS Access Key ID [None]: (press enter to leave empty)
      AWS Secret Access Key [None]: (press enter to leave empty)
      Default region name [None]: us-east-1   
      Default output format [None]: json

    export AWS_ACCESS_KEY_ID="your-access-key"
    export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
    export AWS_SESSION_TOKEN="your-session-token"

    npm install -g @cloud-copilot/iam-collect

    iam-collect init
    iam-collect download --services iam
    ```
  <br />

- **Step 2**: 

    Next, we can choose any of the ```iam-dangerous-actions``` security-risk lists to use: [all-security-risks](https://github.com/ZiyadAlmbasher/iam-dangerous-actions/blob/main/lists/iam-actions-DE-risk.txt), [PE](https://github.com/ZiyadAlmbasher/iam-dangerous-actions/blob/main/lists/iam-actions-PE-risk.txt), [DC](https://github.com/ZiyadAlmbasher/iam-dangerous-actions/blob/main/lists/iam-actions-DC-risk.txt), [DE](https://github.com/ZiyadAlmbasher/iam-dangerous-actions/blob/main/lists/iam-actions-DE-risk.txt) or [HT](https://github.com/ZiyadAlmbasher/iam-dangerous-actions/blob/main/lists/iam-actions-HT-risk.txt). 
    
    In this example, we will use the list ```iam-actions-all-risks.txt```, which includes **all** the IAM actions and their respective [security-risks](https://github.com/ZiyadAlmbasher/iam-dangerous-actions/blob/main/lists/iam-actions-all-risks.txt). 


    ```bash
     cd ~/iam-demo2

     git clone https://github.com/ZiyadAlmbasher/iam-dangerous-actions/ && cd iam-dangerous-actions/scripts 
     
     cp ~/iam-demo2/iam-dangerous-actions/lists/iam-actions-all-risks.txt .
   
    ```
  <br />

- **Step 3**: 

  Now we can choose any IAM policy we would like to audit against our ```iam-actions-all-risks.txt``` list, and copy it over to our working directory: 
  
  ```bash
  ## Make sure to change the AWS account number, and specific IAM policy names accordingly:  
  
  cp ~/iam-demo2/iam-data/aws/aws/accounts/111222333444/iam/policy/<iam_policy_name_lower_case>/current_policy.json ~/iam-demo2/iam-dangerous-actions/scripts/<iam_policy_name_lower_case>.json

  ``` 

  For this demo, the ```dangerous_iam_policy.json``` sample IAM policy **already** exists in the scripts folder. It has the following permissions:

    ```bash
    {
	    "Version": "2012-10-17",
	     "Statement": [
	  	{
		  	"Sid": "SampleDangerousIAMPolicyDoNotUseInProduction",
		  	"Effect": "Allow",
		  	"Action": [
		  		"iam:*",
		  		"lambda:CreateFunction",
			  	"sts:AssumeRole",
				  "cloudfront:ListConflictingAliases",
				  "cloudfront:ListAnycastIpLists",
				  "cloudfront:ListDistributions",
				  "s3:*",
				  "ec2:DescribeAccountAttributes",
				  "ec2:DescribeAddresses",
				  "ec2:DescribeImportSnapshotTasks"
			   ],
		      "Resource": "*"
	    	}
	   ]
   }

   ## Note how "iam:*", "s3:*", and "sts:AssumeRole", coexist with other, less harmful IAM actions, such as "ec2:DescribeAccountAttributes". 
  ```
  <br />

- **Step 4**: 

  Finally, we can now run this AI-generated [python script](https://github.com/ZiyadAlmbasher/iam-dangerous-actions/blob/main/scripts/IAM_cross_checker_SP.py), which will check if there are any ```iam-dangerous-actions``` which also exist in the IAM policy ```dangerous-iam-policy.json```. The script basically provides a summary of all the IAM actions that are present in both files. Let's see it in action:  

    ```bash
    cd ~/iam-demo2/iam-dangerous-actions/scripts/
    

    ## We can either run the python script against the sample IAM policy named dangerous-iam-policy.json which already exists in the scripts folder:  
    
    python3 IAM_cross_checker_SP.py iam-actions-all-risks.txt dangerous-iam-policy.json 
    
    ## OR, run the script and point it directly to an IAM policy as part of the iam-data folder created by iam-collect in Step 1. Dont forget to change the account number and IAM policy name accordingly:  

    python3 IAM_cross_checker_SP.py iam-actions-all-risks.txt ~/iam-demo/iam-data/aws/aws/accounts/111222333444/iam/policy/<iam_policy_name_lower_case>/current-policy.json
    ```

    The script automatically handles IAM actions with wildcards in the IAM policy, and saves the results to a file named ```matched_permissions_SP.txt```. Here is a sample terminal output: 

  ```bash
  ============================================================
  AWS Permission Checker (Enhanced)
  ============================================================

  🔍 Loaded 401 permissions:
   1. "sts:AssumeRole": PE, (DC, DE, HT)
   2. "sts:AssumeRoleWithSAML": PE, (DC, DE, HT)
   3. "sts:AssumeRoleWithWebIdentity": PE, (DC, DE, HT)
  ... and 398 more

  📜 Policy patterns:
   1. iam:*
   2. lambda:createfunction
   3. sts:assumerole
   4. cloudfront:listconflictingaliases
   5. cloudfront:listanycastiplists
   6. cloudfront:listdistributions
   7. s3:*
   8. ec2:describeaccountattributes
   9. ec2:describeaddresses
  10. ec2:describeimportsnapshottasks

  ============================================================
  💡 RESULT: 132 matches found
  ✅ "iam:AddClientIDToOpenIDConnectProvider": PE
  ✅ "iam:AddRoleToInstanceProfile": (PE, DC)
  ✅ "iam:AddUserToGroup": PE
  ... and 129 more 
  ============================================================

  💾 Saved 132 matched permissions to: matched_permissions_SP.txt
  ```

  As we can see, our IAM policy includes 134 **potentially** dangerous IAM actions, where each IAM action has the appropriate security risk(s) assigned to it. Alternatively, we can also use the ```iam-dangerous-actions.txt``` list if we need to have output of IAM Actions and no security risks assigned.  

  <br />

  **Step 5**:   
  Lastly, we can now carefully review to determine the necessity, or potential removal, of these IAM actions, and clean up iam-demo2: 

    ```bash
    cd ~ && rm -rf ~/iam-demo2
    ```


  <br />

  **Notes and considerations**:

  1) Not all AWS services in a given IAM policy will fall under the currently supported [list of services](https://github.com/ZiyadAlmbasher/iam-dangerous-actions/tree/main/supporting-files/current_services.txt) for ```iam-dangerous-actions```.  Due to the vast size of the AWS universe with over 300 services, many AWS services will **not** be included in the future as part of ```iam-dangerous-actions```.

  2) In the dangerous sample IAM policy above (do not use in production!), EC2 was part of the IAM policy, but it is not **yet** part of ```iam-dangerous-actions```.  This reflects the reality that an IAM policy will more than likely include AWS services that are not yet part of ```iam-dangerous-actions```, and that they may or may not be included in the future.  

     In other words, there could be IAM actions under EC2 that are actually dangerous, but would not be flagged as so today. In any case, the three EC2 actions in the dangerous sample IAM policy are ```describe``` in nature and would not be included in the ```iam-dangerous-actions``` lists, even when the EC2 service is added in the near future.     

  3) The current list of planned AWS services to be added can be found [here](https://github.com/ZiyadAlmbasher/iam-dangerous-actions/issues?q=state%3Aopen%20label%3A%22Services-to-add%22).  This [ReadMe section](https://github.com/ZiyadAlmbasher/iam-dangerous-actions?tab=readme-ov-file#List-of-current-AWS-services) explains which AWS services are currently included in ```iam-dangerous-actions```, and how other services are chosen. 


<br />
<br />

Back to the main [iam-dangerous-actions page](https://github.com/ZiyadAlmbasher/iam-dangerous-actions).