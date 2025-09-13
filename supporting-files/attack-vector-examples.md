# Draft mode: examples only                                         
## The completed tool will be done under "iam-security-risks"            


### Security Risk Labels: 
PE = Privilege Escalation                     
DC = Disabling or evasion of Security Controls     
DE = Data Exfiltration                             
HT = Hiding one's Tracks     
NA = Not Applicable. The action will be dangerous when combined with other IAM actions
Note: Direct or primary security risks are not placed in parentheses, whereas indirect or secondary security risks are.


### Actions with risk labels applied: 
"iam:PassRole": PE
"lambda:CreateFunction": NA
"S3:GetObject": DE
"iam:CreateRole": PE             
"iam:PutRolePolicy": PE, (DC, DE, HT)          
"iam:CreatePolicy": PE        
"iam:AttachRolePolicy": PE, (DC, DE, HT)     
"iam:UpdateAssumeRolePolicy": PE, (DC)
"lambda:UpdateFunctionCode": PE, (DC, DE, HT)
"sts:AssumeRole": PE, (DC, DE, HT)


### Evaluation Logic Examples: 

1) Out of all the IAM Roles present in the AWS Account, identify and highlight a high-security risk of DE if the following 
IAM actions are present in the combined policies of an IAM Role: 

   ```
   "iam:PassRole"
   "lambda:CreateFunction"
   "S3:GetObject"
   ```

2) Identify and highlight the critical security risks of PE, DE, HT, and DC if the following IAM actions are collectively present within any IAM Roles in the account:

   ```
   "iam:CreateRole",                
   "iam:PutRolePolicy",              
   "iam:CreatePolicy",           
   "iam:AttachRolePolicy",            
   "iam:UpdateAssumeRolePolicy",
   "lambda:CreateFunction",
   "lambda:UpdateFunctionCode", 
   "sts:AssumeRole"
   ```