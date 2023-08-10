# Zacky_Recon

![image](https://github.com/Gesus-del/Zacky_Recon/assets/79453866/456bf74e-c6ec-4cd3-aafb-bfcc955dd5e1)


Python script for bounty simple life.

## requirements:


* GO:
```bash
sudo apt install golang
```
or just go to the official site
* Subfinder:
```bash
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```
* python3:
```bash
sudo apt install python3
```
* nuclei:
```bash
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
```
* feroxbuster:
```bash
sudo apt update && sudo apt install -y feroxbuster
```
## Usage

Run it with sudo

```bash
sudo python3 zacky_recon.py
```
![image](https://github.com/Gesus-del/Zacky_Recon/assets/79453866/baf009f7-e3f9-4836-a4dc-d15349c21a3d)

It will prompt you to insert 3 things to make the script working:
* the type of scan that will run with nuclei (simple= just nuclei scan(nuclei -l domain.txt) specific= nuclei scan with specific template to usage)
* if the choice is specific you will have to insert the template path

### zap passive scan functionality will be released soon
* the domain to test

After this few things you can chill and take a cofee

