# How is this different from other IAM tools? 

The aim of ```iam-dangerous-actions``` is to simplify IAM management and enhance cloud security. It helps us to achieve this by configuring and auditing IAM actions using a **risk-based** security approach.

The concept behind ```iam-dangerous-actions``` is simple yet powerful: if certain IAM actions can pose major security risks when misused, then why not exclude them from new or existing IAM roles that don't absolutely require them in the first place?

This naturally complies with the principle of least privilege, pre-emptively reducing our AWS security risks significantly.

However, many actions on the dangerous actions lists are legitimately required for business operations and role-based functions. At the very least, the ```iam-dangerous-actions``` lists provide essential visibility into the security risks of each IAM action, enabling informed decision-making when assigning permissions.

The following [real-world use cases](https://github.com/ZiyadAlmbasher/iam-dangerous-actions/blob/main/documentations/real-world-use-cases.md) demonstrate how ```iam-dangerous-actions``` can be used to achieve these objectives. 

<br />
<br />

Back to the main [iam-dangerous-actions page](https://github.com/ZiyadAlmbasher/iam-dangerous-actions).