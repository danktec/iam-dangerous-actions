# How are Security risks assigned to IAM Actions? 


### Security Risk Labels: 
PE = Privilege Escalation                    
DC = Disabling or evasion of Security Controls     
DE = Data Exfiltration                             
HT = Hiding one's Tracks     
NA = Not Applicable. The action will be dangerous when combined with other IAM actions

<br />

Assigning security risks to each IAM action is not as simple as it might seem. There are many challenges and considerations that must be taken into account simultaneously:

- IAM actions can have **direct** (primary) security risks based on their nature, as well as **indirect** (secondary) risks. Let's take a few examples: 

    ```iam:AssumeRoot``` and ```iam:AssumeRole``` have a **direct** security risk of PE. With ```iam:AssumeRoot```, we could transition from having no other IAM actions to having root privileges. Depending on the IAM roles that can be assumed with ```iam:AssumeRole```, we could obtain full admin privileges or other lesser permissions.

    The indirect or secondary risks for both  ```iam:AssumeRoot``` and ```iam:AssumeRole```  would be DC, DE, and HT because these risks could easily be achieved once root or administrator privileges are obtained in the AWS account.


- For IAM actions with both direct and indirect risks, the direct risks are listed without parentheses and the indirect risks follow with parentheses. Here are some examples:

   ```
   "sts:AssumeRole": PE, (DC, DE, HT) --> The primary/direct risk is PE, and the secondary/indirect risks are DC, DE, HT

   "iam:AddRoleToInstanceProfile": (PE, DC) --> Both risks are indirect with no primary risks 

   "sso:CreateApplicationInstanceCertificate": DC --> There is only a DC primary risk
   ```

- In **most** cases, when assessing risks, we consider the worst-case scenario that could result from an IAM action. For example, with ```iam:AssumeRole```, we evaluate the scenario where the user can assume any IAM role, including one with Administrator privileges. 

Although it might be possible for the user to only be able to assume an IAM role with ```read-only permissions```, it would be a massive underestimation of security risks to ignore the possibility that they could assume a role with Admin privileges. Therefore, we will always take the worst-case scenario to cover all possibilities.


- Security risks are interrelated. For example, if a PE risk is present, then DC, DE, and HT risks become highly likely (though not always applicable). Similarly, DC risks can eventually lead to PE, DE, or HT risks by bypassing or evading existing security controls, though this isn't guaranteed. However, HT risks won't directly lead to PE, DE, or DC risks.


- Assigning risks to IAM actions is not an exact science. There is no precise formula to follow because the risk evaluation process relies heavily on risk tolerance and deep understanding of each IAM action's effects and impacts. 

The process depends on multiple factors: whether security risks are achieved directly or indirectly, whether additional IAM actions are required for the risk to materialize, and the evaluator's expertise and consistent reasoning. This subjective nature makes the process inherently prone to error and requires continuous refinement over time.

- Some IAM actions will be labeled as dangerous, but they will receive the risk label NA (Not Applicable). This is because these actions do not pose security risks individually, but they can become dangerous when combined with other actions. These combination-dependent actions will primarily be used in the ```iam-security-risks``` project in the future.

<br />
<br />

Back to the main [iam-dangerous-actions page](https://github.com/ZiyadAlmbasher/iam-dangerous-actions).