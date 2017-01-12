## certbot_py Documentation

##### Current Status: Very Alpha, Proof of Concept

Use at your own peril, until there's some shakedown.

#### Overview

This library is a wrapper around the `certbot`/`certbot-auto` command line tool operating `certonly` in manual, non-interactive mode. It does this via Python's `subprocess.Popen()`.

This allows Python developers to automate the creation of certificates in a web app (ie. Flask or Django). Let's Encrypt's certificate generation process, simplified:

1. `certbot` sends a certificate request for a domain (or multiple domains in the case of SAN/UCC)
2. Let's Encrypt responds with validation instructions for each requested domain
3. For each set of validation instructions, << developer/operations team member needs to manually perform some action - DNS record addition or web server file creation >>
4. Let's Encrypt attempts to validate each domain
5. Upon successful validation, a certificate is provided (either single domain or SAN/UCC)

Step 3 is where this library allows the developer to customize and **automate** their process of setting up validation (see `auth_script` below). This library currently only supports web server validation (ie http-01).

An example scenario where this library becomes useful:
> You have a blogging platform (ie. blog-platform.io) where your customers can sign up and create their own blog (ie. customer1.blog-platform.io).
>
>The Customer would like to host their new blog on their own sub-domain (ie. blog.customer-site.com) for SEO purposes - obviously they want to make sure it's HTTPS enabled.  They can easily do this by adding a CNAME from blog.customer-site.com to customer1.blog-platform.io.
>
> So your blogging platform needs to automatically provision HTTPS certificates as your customers create new blogs and set up CNAMEs for them. `certbot_py` to the rescue.

Please note that there is **NO** mechanism for renewal included; [using `certbot renew` via a cron job is the recommended way](https://certbot.eff.org/docs/using.html#renewing-certificates).

#### Installation

1. You must install `certbot` or `certbot-auto` as you will need to specify the full path to it. It does all the heavy lifting.
2. The user running your Python project code must have access to run `sudo certbot` or `sudo certbot-auto` without a password, which is largely dependent on how you configure your `gunicorn`, `uwsgi`, etc to run (if in a web environment).
    * This likely means running `sudo visudo` or adding an entry to `/etc/sudoers.d/`.
    * **For security, it is highly recommended to only allow `sudo` access to just the one command (`certbot` or `certbot-auto`).**
3. Register an account with Let's Encrypt's servers (if you haven't already). Note that `certbot_py` (this library) defaults to using Let's Encrypt staging servers, while `certbot` and `certbot-auto` default to production servers. An example of registration for staging servers:
   ```
   certbot register --staging
    # OR
   certbot-auto register --staging
   ```
4. In your Python project's virtual environment, install `certbot_py`:
   ```
   pip install certbot_py
   ```

#### Usage

Ensure you register an account with Let's Encrypt, as mentioned above.

There is a single `generate_certificate` method which requires 3 parameters: `domains`, `certbot_command`, and `auth_script`. There are many other optional parameters which mostly map to corresponding `certbot` arguments.

```
from certbot_py import client

command = '/my/path/to/certbot'
script = '/my/other/path/to/auth-hook-script.sh'
my_domains = ['example1.com', 'example2.com', 'example3.com']
results = client.generate_certificate(
    domains=my_domains,
    certbot_command=command,
    auth_script=script
)
```

If you wanted to generate a SAN (ie. UCC) certificate instead, use `san_ucc=True`. As with `certbot`, the first domain in `domains` will be the common name listed on the resulting cert.

```
results = client.generate_certificate(
    domains=my_domains,
    certbot_command=command,
    auth_script=script,
    san_ucc=True
)
```

There are many more options, most of the pertinent ones are listed below.  Skip further down for more information on `auth_script`.

##### Option List

Full list of `generate_certificate` parameters (order is unimportant as they must be passed as keyword arguments):

```
account = None
allow_domain_subset = False
allow_self_upgrade = False
auth_script = None
certbot_command = None
domains = None
hsts = False
must_staple = False
production = False
redirect = False
rsa_key_size = None
san_ucc = False
staple_ocsp = False
uir = False
```

These mostly map to [corresponding `certbot` arguments](https://certbot.eff.org/docs/using.html#certbot-command-line-options), with a few exceptions:

* `production` will enable the live generation of certificates from Let's Encrypt's production servers. By default (and safely), `certbot_py` uses staging servers.
* `san_ucc` indicates that a SAN/UCC certificate is wanted, otherwise an individual cert will be requested for each domain passed in.
* `certbot_command` is the full path the the installed `certbot` or `certbot-auto` command line executable.
* `auth_script` is the full path to a script which will use the `certbot`-provided `$CERTBOT_DOMAIN`, `$CERTBOT_VALIDATION`, and `$CERTBOT_TOKEN` environment variables to perform some developer-specific action (ie. add `$CERTBOT_VALIDATION` and `$CERTBOT_TOKEN` to a database) so that the subsequent validation request from Let's Encrypt's servers can succeed.
* `allow_self_upgrade` would allow auto-upgrading (`certbot-auto` only), which has been disabled by default to prevent breakage due to tool upgrades

Example `auth_script` (Django example), just a single bash script:

```
#~/bin/bash
/home/webuser/.virtualenvs/bin/python /home/webuser/my_project/manage.py set_domain_validation "$CERTBOT_DOMAIN" "$CERTBOT_VALIDATION" "$CERTBOT_TOKEN"
```

##### Command Line

There is a command line alias configured upon `pip install` that you can use to test with. Simply use `certbot_py` on the command line, full help is available.

#### Notes

1. `certbot` version 0.10.0 is the first version to expose the necessary command line arguments - prior versions will fail.
2. This library should be updated for security and bug fixes (obviously) but also may require updating if the underlying arguments to `certbot` change or features are added.

#### Future

Gee, I should mock in some tests...

Longer term, I look forward to having this library change (and improve!) so that it no longer needs Python's `subprocess.Popen()` or a `certbot` installation. This is technically possible using Let's Encrypt's [`acme` library](https://github.com/certbot/certbot/tree/master/acme); however creating a client around `acme` involves much more than something simple like `acme.generate_certificate(...)`. Much in this ACME/Let's Encrypt world seems in flux at the moment, so implementing this wrapper felt like the easiest path forward for the time being - and retains full compatibility with the standard Let's Encrypt command line tools.

Feedback is encouraged and appreciated. [File issues on Github](https://github.com/jaddison/certbot_py/issues). Feel free to fork and suggest improvements.
