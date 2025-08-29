# How are Security risks assigned to IAM Actions? 


### Risk Labels: 
PE = Privilege Escalation                    
DC = Disabling or evasion of Security Controls     
DE = Data Exfiltration                             
HT = Hiding one's Tracks     
NA = Not Applicable. The action will be dangerous when combined with other IAM actions

<br />

Assigning security risks to each IAM action is not as simple as it might seem. Many challenges and considerations that must be taken into account simultaneously:

- IAM actions can have **direct** (primary) security risks based on their nature, as well as **indirect** (secondary) risks. Let's take a few examples: 

    ```iam:AssumeRoot``` and ```iam:AssumeRole``` have a **direct** security risk of PE. With ```iam:AssumeRoot``` , we could transition from having no other IAM actions to having root priviliges. Depending on the IAM roles that can be assumed with ```iam:AssumeRole```, we could obtain full admin privileges or other lesser permissions.

    The indirect or secondary risks for both  ```iam:AssumeRoot``` and ```iam:AssumeRole```  would be DC, DE, and HT because these risks could easily be achieved once root or administrator privileges are obtained in the AWS account.


- For IAM actions with both direct and indirect risks, the direct risks are listed without parentheses and the indirect risks follow with parentheses. Here are some examples:

   ```
   "sts:AssumeRole": PE, (DC, DE, HT) --> The primary/direct risk is PE, and the secondary/indirect risks are DC, DE, HT

   "iam:AddRoleToInstanceProfile": (PE, DC) --> Both risks are indirect with no primary risks 

   "sso:CreateApplicationInstanceCertificate": DC --> There is only a DC primary risk
   ```

- In **most** cases, when assessing risks, we consider the worst-case scenario that could result from an IAM action. For example, with ```iam:AssumeRole```, we assume that the user is able to assume any IAM role, and one of those IAM roles has Administrator priviliges. In security, we usually assume the worst-case scenario that **can** happen, rather than the opposite.

    Although it might be possible for the user to only be able to assume an IAM role with a read-only policy, it would be a massive underestimation of security risks to ignore the possibility that they could not assume a role with admin privileges. Therefore, we will always take the worst-case scenario to cover all possibilities.


- Security risks are interrelated. For example, if a PE risk is present, then DC, DE and HT risks are also highly likely as well (though not always applicable). Similarly, DC risks could eventually lead to PE, DE or even HT risks (by bypassing or evading existing security controls in place), though again, this is not always the case. HT risks won't directly lead to PE, DE, or DC risks.


- Assigning risks to IAM actions is not an exact science. There is no exact formula to follow, because the risk evaluation process itself relies on risk tolerance and a deep understanding of the effects and impacts for each IAM action. The process also depends on whether security risks are achieved directly or indirectly,  and on whether any additional IAM actions are required or not in order for the risk to materialize. In other words, this process depends on expertise and consistent reasoning. However, this also makes the process prone to error and requires continuous refinement.


- Some IAM actions will be labeled as dangerous, but they will not have a risk label (NA). This is because, while these actions do not pose a security risk on their own, they can when combined with other actions. These actions will mostly be used in the ```iam-security-risks``` project in the future.


<br />
<br />

Back to the main [iam-dangerous-actions page](https://github.com/ZiyadAlmbasher/iam-dangerous-actions).
