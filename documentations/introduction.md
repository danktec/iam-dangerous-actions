# Introduction

There are **many** reasons why managing and implementing IAM correctly can be challenging.

Every Identity-based principal, AWS Service-role, federated Identity provider, and permission-set relies on IAM actions to function properly. This puts IAM Roles, and therefore IAM policies, at the very top list of our AWS Cloud security agenda, goals and efforts.  

Assigning too many IAM actions to IAM Roles poses major security risks. Conversely, adding too few IAM actions can hinder operations, slow down innovation and product delivery. 

Currently, there are over 18,000 IAM actions across more than 300 AWS services.

Large organisations' projects and solutions require the careful assignment of hundreds or even thousands of these IAM actions.

```iam-dangerous-actions``` aims to help us identify which IAM actions are dangerous and should be approached with caution when creating new, or auditing existing IAM policies, and therefore, IAM Roles. The goal is to reduce security risks related to IAM Role permissions.

This will solve some of our IAM problems by reducing many security threats from the early stages.

<br />
<br />

Back to the main [iam-dangerous-actions page](https://github.com/ZiyadAlmbasher/iam-dangerous-actions). 
