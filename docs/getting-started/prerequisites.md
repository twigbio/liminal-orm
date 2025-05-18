1. **Benchling Admin Account**: Liminal builds on top of Benchling's LIMS system. You will need access and credentials to an admin account for your Benchling tenant(s). Liminal needs credentials with full admin priveleges in order to manipulate Benchling schemas through their API.

2. **SSO optional**: A requirement for Liminal's migration service to work is for your Benchling tenant to have SSO optional (or disabled). At the moment, a part of Liminal's API connection requires an admin email and password login (non-SSO). You can message Benchling support to request that your tenant be configured to be SSO optional (or disabled).

Note that as a Benchling admin, you can enforce SSO for all users and create only a single non-SSO user for Liminal to use. This is what we recommend to maintain the highest level of security.

3. **Python**: Liminal is built using Python. You will need Python 3.9 or later installed on your machine.

### Notes

- Liminal currently supports coverage for Benchling entity schemas, results schemas, and dropdowns at the moment. Leave a comment on the [Discussions](https://github.com/dynotx/liminal-orm/discussions) forum on your vote for what should be supported next, or what is blocking you from using Liminal!
