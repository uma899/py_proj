with open("test.html", 'w') as file:
    file.write("<html>\n")
    file.write("<head><title>test</title><style>body {font-family: Verdana} h3 {font-weight: \"500\"; display: inline-block}</style><head>\n")
    file.write("<body>\n")

temp = ""
c1 = 0
c2 = 0
with open("myFile.txt", 'r') as file:
    for line in file:
        for i in line:
            if i=="\"":
                if c1==0:
                    temp = temp + "<h1>"
                    c1 = 1
                else:
                    temp = temp + "</h1>"
                    c1 = 0 # Corrected: This line now correctly aligns with the 'temp' line above it
            elif i=="\'": # Corrected: This 'elif' now aligns with the 'if' above it
                if c2==0:
                    temp = temp + "<h3>"
                    c2 = 1
                else:
                    temp = temp + "</h3>"
                    c2 = 0 # Corrected: This line now correctly aligns with the 'temp' line above it
            else: # Corrected: This 'else' now aligns with the 'if' above it
                temp = temp + i

with open("test.html", 'a') as file: # Corrected: Now appends to test.html, not myFile.txt
    file.write(temp+"\n")
    file.write("</body>\n</html>")