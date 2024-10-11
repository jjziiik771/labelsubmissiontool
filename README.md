# LABEL SUBMISSION WEB TOOL
### Use with responsability

1. clone this repo
2. Create virtual env 
```
python -m venv venv

```

3. activate (depending of your OS)
###### Windows
```
.\env\Scripts\activate 

```
###### MacOs/Linux
```
source venv/bin/activate

```
4. Install dependencies
```
pip install -r requirements.txt

```
5. Run Server 
```
uvicorn main:app --reload
```
!!! Frontend built with React+Tailwind compiled into static/dist files
##### app/static/index
     - give the Password a name and click "create"
     - write down the key you see in a blue box since you are not able to see it ever again
     - put this exact code into the Google App Code Box inside the tool

7. Press Submit and everything should work (if not, the error will be shown or available in the log.txt file in the same directory as the submission tool)


If you have any questions or encounter any bugs, you can contact me on my social here: https://linktr.ee/TakumoZero
