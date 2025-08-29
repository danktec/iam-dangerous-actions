
# What is the difference between "dangerous" and "high privilege" actions? 


In this context, we define **high-privilege** actions as those that have a significant impact and wide scope. 

Examples include Admin policies, or policies containing many services with wildcards, such as `"iam:*", "Lambda:*", and "sso:*"`. 

Although **dangerous** IAM actions are inherently part of high-privilege actions, they differ in the following characteristics:

* They do not need to be numerous or contain wildcards. However, they are very powerful and impactful, especially when combined together.
* They can easily go unnoticed alongside less dangerous IAM actions, such as List and Get.
* They focus on **security** risks to production data, environments and architectures.

<br />
<br />

Back to the main [iam-dangerous-actions page](https://github.com/ZiyadAlmbasher/iam-dangerous-actions).
