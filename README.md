# volto plantillak

Repositorio honetan Volto proiketu bat hasieratzean kontuan eduki beharreko gauzak azalduko ditugu.

## Proiektuaren osaera

Gure proiektuek 2 pakete eta 2 errepositorio izango dituzte:

* `XXXX-frontend`: proiektuaren repositorioa: hemen Volto instalatuko da eta dependentzia eta konfigurazio orokorrak zehaztuko dira

* `volto-XXXX`: pertsonalizazio paketea: hemen proiektu zehatz honi dagozkion estilo pertsonalizazioak eta pertsonalizazioak joango dira.
    
## Nola sortu hasierako paketeak

### XXX-frontend

EEAren proiektuaren txantiloia erabiliko dugu. Horretarako zera egin behar da:

* gitlab-en gure proiektuaren errepositorioa sortu: izena `XXXX-frontend` izan dadila, ez sortu README fitxategirik bertan (checkbox bat dago hori aukeratzeko)
* https://github.com/eea/volto-frontend-template orrialdera joan eta **Use this template** botoia sakatu
* codesyntax errepositorioan sortu pakete proiektuaren errepositorioa dagokion izena jarriz, adibidez: `codesyntax-frontend`
* errepositorio hori gure makinara klonatu:
    ```bash
    git clone git@github.com:codesyntax/codesyntax-frontend
    ```
* komando hauek exekutatu proiektua abiarazteko:
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
* Repositorio honetan dagoen [frontend-txantiloia](frontend-txantiloia) karpetaren edukiak deskargatu eta sortu berri dugun errepositoriora gehitu.

* Aldaketak errepositoriora igo:
    ```bash
    git add .
    git commit -m "CI-CD configuration"
    git push origin main
    ```
* Gitlaben repositorioa konfiguratu, ireki https://gitlab.com/codesyntax/codesyntax-frontend:    
    * **Settings** -> **Repository** -> **Deploy keys** -> **Expand** sakatu. **Privately accesible deploy keys** fitxara joan eta **volto-ssh-deploy-key** agertzen denaren ondoko **Enable** botoia sakatu. Hau egiterakoan **Enabled deploy keys** fitxara pasatuko da. Fitxa horretan bere ondoan dagoen arkatzaren ikonoa sakatu eta **Grant write permissions to this key** checkboxa aukeratu
    
    * **Settings** -> **Repository** -> **Protected branches** -> **Expand** sakatu. **main** adarra defektuz babestuta agertuko da. **Allowed to push** desplegablean kendu aukeratuta dagoen **Maintainers** eta **Deploy Keys** azpian dagoen **volto-ssh-deploy-key** aukeratu.
    
    * **Settings** -> **CI/CD** -> **Variables** -> **Expand** sakatu. Bi aldagai berri gehitu:
        * SSH_SERVER_NAME: balioa zerbitzariaren domeinu izena (adb: `deba.korpoweb.com`), **Protected** ez aukeratu eta **Masked** ere ez.
        * VOLTO_SUPERVISOR_NAME: balioa normalean `voltoproiektuizena` izaten da, begiratu buildoutak supervisorrean zer sortu duen, hau voltoa berrabiarazteko erabiltzen da.
        
* Zerbitzari berriarekin Gitlaben konfigurazio orokorra aldatu: volto proiektu hau zerbitzari batera jargatu behar dugunean, zerbitzari horren SSH gakoa zein den esan behar diogu Gitlabi, SSH konexioak ondo egiteko. Horretarako joan helbide honetara: https://gitlab.com/codesyntax
    * Gure makinatik `ssh-keyscan -t rsa zerbitzaria.korpoweb.com` exekutatu eta emaitza gisa txurro bat irtengo da. Txurro hori kopiatu VisualCodera eta **lerro bakarrean utzi**. Hurrengo pausoan erabiliko dugu.
    * **Settings** -> **CI/CD** -> **Variables** -> **Expand** sakatu. **SSH_KNOWN_HOSTS** aldagaiaren balioa editatu eta lerro berri baten aurreko pausuko gakoa kopiatu.

    
Aldaketa hauekin proiektua prest egongo da Merge-Request bat dagoenean `yarn build` exekutatzeko eta erroreak badaude merge-request-ean bertan adierazteko.

Merge-request-a onartzen denean bertsio berri bat aterako du, CHANGELOGa bete, tag berri bat sortuko du eta automatikoki eguneratu egingo du zerbitzarian.


### volto-XXXX

Honetarako ere EEAren volto addon baten txantiloia erabiliko dugu.

* gitlaben gure addonaren errepositorioa sortu: izena `volto-XXXX` izan dadila, ez sortu README fitxategirik bertan (checkbox bat dago hori aukeratzeko)

* https://github.com/eea/volto-addon-template orrialdera joan eta **Use this template** botoia sakatu.

* codesyntax errepositoriaon sortu addonari dagokion izena jarriz, adibidez: `volto-codesyntax`.

* errepositorio hori gure makinara klonatu:
    ```bash
    git clone git@github.com:codesyntax/volto-codesyntax
    ```
* komando hauek exekutatu addona abiarazteko:
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

* Repositorio honetan dagoen [volto-txantiloia](volto-txantiloia) karpetaren edukiak deskargatu eta sortu berri dugun errepositoriora gehitu

* `package.json` fitxategia editatu eta bukaeran hau gehitu:
    ```json
  "publishConfig": {
        "registry": "https://code.codesyntax.com/npm/"
  }
  ```

* Aldaketak errepositoriora igo:
    ```bash
    git add .
    git commit -m "CI-CD configuration"
    git push origin main -u
    ```
* Gitlaben repositorioa konfiguratu, ireki https://gitlab.com/codesyntax/volto-codesyntax:    
    * **Settings** -> **Repository** -> **Deploy keys** -> **Expand** sakatu. **Privately accesible deploy keys** fitxara joan eta **volto-ssh-deploy-key** agertzen denaren ondoko **Enable** botoia sakatu. Hau egiterakoan **Enabled deploy keys** fitxara pasatuko da. Fitxa horretan bere ondoan dagoen arkatzaren ikonoa sakatu eta **Grant write permissions to this key** checkboxa aukeratu
    
    * **Settings** -> **Repository** -> **Protected branches** -> **Expand** sakatu. **main** adarra defektuz babestuta agertuko da. **Allowed to push** desplegablean kendu aukeratuta dagoen **Maintainers** eta **Deploy Keys** azpian dagoen **volto-ssh-deploy-key** aukeratu.
    
Aldaketa hauekin Merge-Request bat onartzen denean bertsio berri bat aterako du, CHANGELOGa bete, tag berri bat sortuko eta https://code.codesyntax.com/npm/ -ra kargatuko du.    

**ADI**: ondoren eskuz aldatu beharko da XXXX-frontend paketearean `package.json` fitxategian bertsio berria.

**TO-DO**: bertsio aldaketa hau automatikoki egitea pendiente dago.

## Garapenerako jarraibideak

Jarraibide orokor gisa EEAren proiektuetan erabiltzen dugun gitflow metodologia erabiliko dugu:

- Garapenak `develop` izeneko adar baten edo `develop` adarretik ateratako adar berri baten egingo dira.
- Bertsio berriak sortzeko prest gaudenean Merge Request bat egin behar da `develop` adarretik `main` adarrera.
- `XXXX-frontend` paketearen kasuan, Merge Request-a ezin da onartu, bertan konfiguratuta dagoen testa exekutatu arte. Test horrek `yarn` eta `yarn build` exekutatzen ditu, horrela ondorengo argitaraketa ondo joango dela bermatzen du. Merge Request baten adibidea hemen: https://gitlab.com/codesyntax/deba-frontend/-/merge_requests/5
- Arazoak eskuz debugeatu nahi baditugu, `yarn build` komandoaren emaitza "artifact" bezala gordeta gelditzen da eta berau deskargatu eta eskuz probatu dezakegu. Hemen dago adibide bat: https://gitlab.com/codesyntax/deba-frontend/-/merge_requests/5 Hor erdian dago Merge Requestaren emaitza **Detached merge request pipeline** dioen tokian, lerro bukaeran dagoen deskargarako botoiarekin deskargatu dezakegu `yarn build`en emaitza.

Pakete publiko berrerabilgarriren bat egiten hasten bagara, berau GitHuben kargatuko dugu. Bere argitaraketak automatizatu ditzakegu, horretarako [volto-listingadvanced-variation](https://github.com/codesyntax/volto-listingadvanced-variation) paketean dagoen `.github` izeneko karpeta eta bere edukiak sortu beharko ditugu pakete berrian (adi `.github` karpetaren barruan `workflows` izeneko bat egon behar da eta bere barruan `release.yml` fitategia) eta `develop` adarretik `main` adarrerako pull-requestak erabili. Argitaraketak NPMn egiteko beharrezko tokenak `codesyntax` mailan ezarrita daude eta ez da konfigurazio berezirik egin behar.
