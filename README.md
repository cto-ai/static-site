![](assets/banner.png)

# Deploying S3 Static Site Deployment

An interactive Op that deploys a static site to a public S3 bucket.

## Requirements

To run this or any other Op, install the [Ops Platform](https://cto.ai/platform).

Find information about how to run and build Ops via the [Ops Platform Documentation](https://cto.ai/docs/overview).

This Op also requires AWS credentials to work with your account. Here's what you'll need before running this Op the first time:

- **AWS Access Key Id**: via the [AWS Management Console](https://console.aws.amazon.com/):
  - `AWS Management Console` -> `Security Credentials` -> `Access Keys`
- **AWS Access Key Secret**: via the [AWS Management Console](https://console.aws.amazon.com/):
  - `AWS Management Console` -> `Security Credentials` -> `Access Keys`

## Usage

The very first time you run this Op, you'll want to set up the appropriate secrets so you don't have to manually enter it in each time.

To set secrets, run:

```bash
ops secrets:set
```

Follow the prompts and enter in the name of the key and its value. This will save the secret so it can be accessed the next time you use the Op.

This will set the secret to the team which you're currently on (The default is your personal team which is the same as your username). You can also check which team you're currently on by running:

```bash
ops whoami
```

In order to use the secrets you just set, the Op needs to be published to this team.

To run the public version of the Op in the terminal, enter in:

```bash
ops run @cto.ai/static-site
```

To run the public version of the Op in a public Slack channel:

```bash
ops run cto.ai/repo
```

## Local Development / Running from Source

**1. Clone the repo:**

```bash
git clone <git url>
```

**2. Navigate into the directory and build the image:**

```bash
cd static-site && ops build .
```

**3. Run the Op from your current working directory with:**

```bash
ops run .
```

**4. To publish the Op to your team:**

```bash
ops publish .
```
To run the Op in Slack, make sure that you have the [CTO.ai Bot](https://cto.ai/platform) installed
in your Slack workspace.

To run the Op in a Slack channel, enter:
`/ops run static-site`

## Debugging Issues

When submitting issues or requesting help, be sure to also include the version information. To get your Ops version run:

```bash
ops -v
```

You can reach us at the [CTO.ai Community Slack](https://cto-ai-community.slack.com/) or email us at support@cto.ai.

## AWS Documents

- [Getting Started on Amazon Web Services (AWS)](https://aws.amazon.com/getting-started/)
- [AWS SDK for Python (Boto3) Reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html)

## Contributing

See the [Contributing Docs](CONTRIBUTING.md) for more information

## Contributors

- **Dillon Hung** via [GitHub](https://github.com/dhungdata)

## LICENSE

[MIT](LICENSE.txt)
