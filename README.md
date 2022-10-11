# volto plantillak

- [English](#english)
- [Euskara](#euskara)

# English

In this repo you will find the files required in a Volto project setup.

## Gitlab project configuration

We need to create the following variables in our Gitlab organization:

- CI_GITLAB_USER_EMAIL: the email belonging to the user who will be used to commit the changes made by release-it.
- CI_GITLAB_USERNAME: the username which will be used to commit the changes made by release-it
- CODESYNTAX_NPM_REPO_URL: the URL of the private npm registry
- CODESYNTAX_REPO_NPM_TOKEN: the token needed to publish packages in the private npm registry
- GITLAB_TOKEN: a gitlab token created by a user of the organization which will be used to commit and push the changes.
- MJ_APIKEY_PRIVATE: private key of the Mailjet API, used to send emails
- MJ_APIKEY_PUBLIC: public key of the Mailjet API, used to send emails
- SSH_KNOWN_HOSTS: list of the rsa keys of the servers known to gitlab ci so the changes can be deployed.
- SSH_SERVER_BUILDOUT_PATH: path to the buildout where the plone and volto installation lie in the server.
- SSH_SERVER_USER: user tha is used to scp the changes to the server
- VOLTO_DEPLOY_SSH_PRIVATE_KEY: private key used to deploy the volto project to the server. The corresponding public key must be added at `~/.ssh/authorized_keys` in the server.
- VOLTO_RELEASE_EMAIL_TO: email address to which the success email will be sent.

## Project composition

Our projects will have 2 packages and 2 repositories:

- `XXXX-frontend`: project repo: this will handle the Volto installation and all main dependencies.

- `volto-XXXX`: customization addon: this package will contain the custom blocks, configurations and dependencies.

## How to create the packages

We will be using EEA's template repos to create our packages

### XXX-frontend

- go to gitlab and create the repo: use `XXXX-frontend` as name, do not create a README (there is a checkbox for that)
- go to https://github.com/eea/volto-frontend-template and click on **Use this template**
- create a new repo in your github and name it as `XXXX-frontend`
- clone this repo to your laptop
  ```bash
  git clone git@github.com:codesyntax/XXXX-frontend
  ```
- execute these commands to prepare the project:
  ```bash
  cd codesyntax-frontend
  nvm install lts/fermium
  nvm use lts/fermium
  npm install -g yo @plone/generator-volto ejs
  npm install ejs
  rm -rf package.json package-lock.json
  yo @plone/volto --skip-install --workspace src/addons/*
  # Answer the questions: name it xxxx-frontend (project name) and set addons to false
  node bootstrap
  git checkout -b main
  git add .
  git commit -m "Initial commit"
  git remote rm origin
  git remote add origin git@gitlab.com:username/xxxx-frontend
  git push origin main -u
  ```
- Download the [update-templates.py](update-templates.py) to the repo and execute it to download the required templates:
  ```bash
  python3 update-templates.py -frontend
  ```
- Upload the changes to your repo:

  ```bash
  git add .
  git commit -m "CI-CD configuration"
  git push origin main
  ```

- Configure the repo in Gitlab, open https://gitlab.com/organization/XXXX-frontend:

  - **Settings** -> **Repository** -> **Deploy keys** -> **Expand**. Go to **Privately accesible deploy keys** and **Enable** **volto-ssh-deploy-key** . On doing this it will jump to the **Enabled deploy keys** tab. Click on the pen icon and select the checkbox **Grant write permissions to this key**

  - **Settings** -> **Repository** -> **Protected branches** -> **Expand**. The **main** branch will be selected. Unselect the **Maintainers** in the **Allowed to push** dropdown and select the **volto-ssh-deployley** under **Deploy Keys**.

  - **Settings** -> **CI/CD** -> **Variables** -> **Expand**. Add two new vars:

    - SSH_SERVER_NAME: the name of the server (ex: `project.korpoweb.com`), do not select **Protected** and **Masked**.
    - VOLTO_SUPERVISOR_NAME: normally this will be `voltoprojectname` but check the name in the supervisor you are using.

  - **Settings** -> **General** -> **Merge requests** -> **Expand**. Disable **Enable "Delete source branch" option by default** under **Merge options**.

- Set the server configuration. Get the SSH key of the server. Go to https://gitlab.com/user:
  - Execute `ssh-keyscn -t rsa server.korpoweb.com` and copy the rsa key in **one line**.
  - **Settings** -> **CI/CD** -> **Variables** -> **Expand**. Edit the value of **SSH_KNOWN_HOSTS** and add the key you got in the previous step in a new line.

With these changes the project will be ready to build itself when there is a Merge Request to **main** branch. If there is any error it will be reported in the Merge Request itself.

When the Merge Request is accepted a new version will be prepared, the CHANGELOG updated, a new tag and release created and the server will be updated automatically.

### volto-XXXX

- create the repo in Gitlab and name it `volto-XXXX`. Do not create a README.

- Go to https://github.com/eea/volto-addon-template and use the button **Use this template**.

- Create a repo in your organization account with a name like `volto-XXXX`

- clone the repo to your laptop:

  ```bash
  git clone git@github.com:organization/volto-XXXX
  ```

- execute these commands:

  ```bash
  cd volto-codesyntax
  nvm install lts/fermium
  nvm use lts/fermium
  npm i -g yarn
  yarn bootstrap
  git checkout -b main
  git add .
  git ci -m "initial commit"
  git remote rm origin
  git remote add origin git@gitlab.com:organization/volto-codesyntax
  git push origin main -u
  ```

- download the [update-templates.py](updates-templates.py) script in this repo and execute it:

  ```bash
  python3 update-template.py -theme
  ```

- upload the changes to the repo:
  ```bash
  git add .
  git commit -m "CI-CD configuration"
  git push origin main -u
  ```
- Configure the repo in Gitlab, open https://gitlab.com/organization/volto-XXXX:

  - **Settings** -> **Repository** -> **Deploy keys** -> **Expand**. Go to **Privately accesible deploy keys** and **Enable** **volto-ssh-deploy-key** . Doing this the option will go to the **Enabled deploy keys** tab. Click on the pen icon and select the checkbox **Grant write permissions to this key**

  - **Settings** -> **Repository** -> **Protected branches** -> **Expand**. The **main** branch will be selected. Unselect the **Maintainers** in the **Allowed to push** dropdown and select the **volto-ssh-deployley** under **Deploy Keys**.

  - **Settings** -> **CI/CD** -> **Variables** -> **Expand**. Add two new vars:

    - SSH_SERVER_NAME: the name of the server (ex: `project.korpoweb.com`), do not selected **Protected** and **Masked**.
    - VOLTO_SUPERVISOR_NAME: normally this will be `voltoprojectname` but check the name in the supervisor you are using.

  - **Settings** -> **General** -> **Merge requests** -> **Expand**. Disable **Enable "Delete source branch" option by default** under **Merge options**.

With these changes when a Merge-Request is accepted a new version will be released, tagged, CHANGELOG updated and uploaded to the private registry at https://code.codesyntax.com/npm/

**WARNING**: after the release you will need to update the package version manually in your XXXX-frontend package.

## Development notes

The development flow is the following:

- The developments will be made in a branch called `develop` or in branches created from this `develop` branch and merged back there.

- When we are ready to create a new version a Merge Request will be created from `develop` to `main`.

- In the `XXXX-frontend` package the Merge Request can't be accepted until the `yarn build` is succesful and this guarantees that the release will be done correctly.

- If we want to debug the results of `yarn build` the build is saved as an artifact so that it can be downloaded.

# Euskara

Repositorio honetan Volto proiketu bat hasieratzean kontuan eduki beharreko gauzak azalduko ditugu.

## Proiektuaren osaera

Gure proiektuek 2 pakete eta 2 errepositorio izango dituzte:

- `XXXX-frontend`: proiektuaren repositorioa: hemen Volto instalatuko da eta dependentzia eta konfigurazio orokorrak zehaztuko dira

- `volto-XXXX`: pertsonalizazio paketea: hemen proiektu zehatz honi dagozkion estilo pertsonalizatuak eta pertsonalizazioak joango dira.

## Nola sortu hasierako paketeak

### XXX-frontend

EEAren proiektuaren txantiloia erabiliko dugu. Horretarako zera egin behar da:

- gitlab-en gure proiektuaren errepositorioa sortu: izena `XXXX-frontend` izan dadila, ez sortu README fitxategirik bertan (checkbox bat dago hori aukeratzeko)
- https://github.com/eea/volto-frontend-template orrialdera joan eta **Use this template** botoia sakatu
- codesyntax errepositorioan sortu pakete proiektuaren errepositorioa dagokion izena jarriz, adibidez: `codesyntax-frontend`
- errepositorio hori gure makinara klonatu:
  ```bash
  git clone git@github.com:codesyntax/codesyntax-frontend
  ```
- komando hauek exekutatu proiektua abiarazteko:
  ```bash
  cd codesyntax-frontend
  nvm install lts/fermium
  nvm use lts/fermium
  npm install -g yo @plone/generator-volto ejs
  npm install ejs
  rm -rf package.json package-lock.json
  yo @plone/volto --skip-install --workspace src/addons/*
  # Galderei erantzun: izena: codesyntax-frontend (proiektuaren izena) eta addons: false
  node bootstrap
  git checkout -b main
  git add .
  git commit -m "Initial commit"
  git remote rm origin
  git remote add origin git@gitlab.com:codesyntax/codesyntax-frontend
  git push origin main -u
  ```
- Repositorio honetan dagoen [update-templates.py](update-templates.py) deskargatu zure repora eta exekutatu:

  ```bash
  python3 update-templates.py -frontend
  ```

- Aldaketak errepositoriora igo:
  ```bash
  git add .
  git commit -m "CI-CD configuration"
  git push origin main
  ```
- Gitlaben repositorioa konfiguratu, ireki https://gitlab.com/codesyntax/codesyntax-frontend:

  - **Settings** -> **Repository** -> **Deploy keys** -> **Expand** sakatu. **Privately accesible deploy keys** fitxara joan eta **volto-ssh-deploy-key** agertzen denaren ondoko **Enable** botoia sakatu. Hau egiterakoan **Enabled deploy keys** fitxara pasatuko da. Fitxa horretan bere ondoan dagoen arkatzaren ikonoa sakatu eta **Grant write permissions to this key** checkboxa aukeratu

  - **Settings** -> **Repository** -> **Protected branches** -> **Expand** sakatu. **main** adarra defektuz babestuta agertuko da. **Allowed to push** desplegablean kendu aukeratuta dagoen **Maintainers** eta **Deploy Keys** azpian dagoen **volto-ssh-deploy-key** aukeratu.

  - **Settings** -> **CI/CD** -> **Variables** -> **Expand** sakatu. Bi aldagai berri gehitu:

    - SSH_SERVER_NAME: balioa zerbitzariaren domeinu izena (adb: `proiektua.korpoweb.com`), **Protected** ez aukeratu eta **Masked** ere ez.
    - VOLTO_SUPERVISOR_NAME: balioa normalean `voltoproiektuizena` izaten da, begiratu buildoutak supervisorrean zer sortu duen, hau voltoa berrabiarazteko erabiltzen da.

  - **Settings** -> **General** -> **Merge requests** -> **Expand** sakatu. **Merge options** atalean desaktibatu **Enable "Delete source branch" option by default**, defektuz markatuta datorrena.

- Zerbitzari berriarekin Gitlaben konfigurazio orokorra aldatu: volto proiektu hau zerbitzari batera jargatu behar dugunean, zerbitzari horren SSH gakoa zein den esan behar diogu Gitlabi, SSH konexioak ondo egiteko. Horretarako joan helbide honetara: https://gitlab.com/codesyntax
  - Gure makinatik `ssh-keyscan -t rsa zerbitzaria.korpoweb.com` exekutatu eta emaitza gisa txurro bat irtengo da. Txurro hori kopiatu VisualCodera eta **lerro bakarrean utzi**. Hurrengo pausoan erabiliko dugu.
  - **Settings** -> **CI/CD** -> **Variables** -> **Expand** sakatu. **SSH_KNOWN_HOSTS** aldagaiaren balioa editatu eta lerro berri baten aurreko pausuko gakoa kopiatu.

Aldaketa hauekin proiektua prest egongo da Merge-Request bat dagoenean `yarn build` exekutatzeko eta erroreak badaude merge-request-ean bertan adierazteko.

Merge-request-a onartzen denean bertsio berri bat aterako du, CHANGELOGa bete, tag berri bat sortuko du eta automatikoki eguneratu egingo du zerbitzarian.

### volto-XXXX

Honetarako ere EEAren volto addon baten txantiloia erabiliko dugu.

- gitlaben gure addonaren errepositorioa sortu: izena `volto-XXXX` izan dadila, ez sortu README fitxategirik bertan (checkbox bat dago hori aukeratzeko)

- https://github.com/eea/volto-addon-template orrialdera joan eta **Use this template** botoia sakatu.

- codesyntax errepositoriaon sortu addonari dagokion izena jarriz, adibidez: `volto-codesyntax`.

- errepositorio hori gure makinara klonatu:
  ```bash
  git clone git@github.com:codesyntax/volto-codesyntax
  ```
- komando hauek exekutatu addona abiarazteko:

  ```bash
  cd volto-codesyntax
  nvm install lts/fermium
  nvm use lts/fermium
  npm i -g yarn
  yarn bootstrap
  git checkout -b main
  git add .
  git ci -m "initial commit"
  git remote rm origin
  git remote add origin git@gitlab.com:codesyntax/volto-codesyntax
  git push origin main -u
  ```

- Repositorio honetan dagoen [volto-txantiloia](volto-txantiloia) karpetaren edukiak deskargatu eta exekutatu:

  ```bash
  python3 update-template.py -theme
  ```

- Aldaketak errepositoriora igo:
  ```bash
  git add .
  git commit -m "CI-CD configuration"
  git push origin main -u
  ```
- Gitlaben repositorioa konfiguratu, ireki https://gitlab.com/codesyntax/volto-codesyntax:

  - **Settings** -> **Repository** -> **Deploy keys** -> **Expand** sakatu. **Privately accesible deploy keys** fitxara joan eta **volto-ssh-deploy-key** agertzen denaren ondoko **Enable** botoia sakatu. Hau egiterakoan **Enabled deploy keys** fitxara pasatuko da. Fitxa horretan bere ondoan dagoen arkatzaren ikonoa sakatu eta **Grant write permissions to this key** checkboxa aukeratu

  - **Settings** -> **Repository** -> **Protected branches** -> **Expand** sakatu. **main** adarra defektuz babestuta agertuko da. **Allowed to push** desplegablean kendu aukeratuta dagoen **Maintainers** eta **Deploy Keys** azpian dagoen **volto-ssh-deploy-key** aukeratu.

  - **Settings** -> **General** -> **Merge requests** -> **Expand** sakatu. **Merge options** atalean desaktibatu **Enable "Delete source branch" option by default**, defektuz markatuta datorrena.

Aldaketa hauekin Merge-Request bat onartzen denean bertsio berri bat aterako du, CHANGELOGa bete, tag berri bat sortuko eta https://code.codesyntax.com/npm/ -ra kargatuko du.

**ADI**: ondoren eskuz aldatu beharko da XXXX-frontend paketearean `package.json` fitxategian bertsio berria.

**TO-DO**: bertsio aldaketa hau automatikoki egitea pendiente dago.

## Garapenerako jarraibideak

Jarraibide orokor gisa EEAren proiektuetan erabiltzen dugun gitflow metodologia erabiliko dugu:

- Garapenak `develop` izeneko adar baten edo `develop` adarretik ateratako adar berri baten egingo dira.
- Bertsio berriak sortzeko prest gaudenean Merge Request bat egin behar da `develop` adarretik `main` adarrera.
- `XXXX-frontend` paketearen kasuan, Merge Request-a ezin da onartu, bertan konfiguratuta dagoen testa exekutatu arte. Test horrek `yarn` eta `yarn build` exekutatzen ditu, horrela ondorengo argitaraketa ondo joango dela bermatzen du.
- Arazoak eskuz debugeatu nahi baditugu, `yarn build` komandoaren emaitza "artifact" bezala gordeta gelditzen da eta berau deskargatu eta eskuz probatu dezakegu.

Pakete publiko berrerabilgarriren bat egiten hasten bagara, berau GitHuben kargatuko dugu. Bere argitaraketak automatizatu ditzakegu, horretarako [volto-listingadvanced-variation](https://github.com/codesyntax/volto-listingadvanced-variation) paketean dagoen `.github` izeneko karpeta eta bere edukiak sortu beharko ditugu pakete berrian (adi `.github` karpetaren barruan `workflows` izeneko bat egon behar da eta bere barruan `release.yml` fitategia) eta `develop` adarretik `main` adarrerako pull-requestak erabili. Argitaraketak NPMn egiteko beharrezko tokenak `codesyntax` mailan ezarrita daude eta ez da konfigurazio berezirik egin behar.
