<?xml version="1.0" encoding="utf-8" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:import href="parameters.xsl" />

<xsl:output method="html" encoding="UTF-8" omit-xml-declaration="yes" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" indent="yes" cdata-section-elements="script"/>

<xsl:template match="/clam">
  <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <xsl:call-template name="head" />
  <body>
    <div id="container">
        <div id="header"><h1><xsl:value-of select="@name"/></h1><h2><xsl:value-of select="@project"/></h2></div>
        <xsl:apply-templates select="status"/>
        <xsl:choose>
          <xsl:when test="status/@code = 0">              
            <xsl:apply-templates select="input"/>
            <!-- upload form transformed from input formats -->
            <xsl:apply-templates select="inputformats"/>             
            <xsl:apply-templates select="parameters"/>  
          </xsl:when>
          <xsl:when test="status/@code = 2">
            <xsl:apply-templates select="output"/>
          </xsl:when>
        </xsl:choose>
        <xsl:call-template name="footer" />
    </div>
  </body>
  </html>
</xsl:template>


<xsl:template name="head">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <xsl:if test="status/@code = 1">
      <meta http-equiv="refresh" content="10" />            
    </xsl:if>
    <title><xsl:value-of select="@name"/> :: <xsl:value-of select="@project"/></title>
    <link rel="stylesheet" href="/static/style.css" type="text/css" />
    <script type="text/javascript" src="/static/jquery-1.4.2.min.js"></script>
    <script type="text/javascript">
     $(document).ready(function(){
       if ($("#startprojectbutton").length) {
           $("#startprojectbutton").click(function(event){
             $.ajax({ 
                type: "PUT", 
                url: "/" + $("#projectname").val() + "/", 
                dataType: "xml", 
                complete: function(xml){ 
                    window.location.href = $("#projectname").val() + "/";
                },
             });
             //$("#startprojectform").attr("action",$("#projectname").val());
           });
       }
       if ($("#abortbutton").length) {
           $("#abortbutton").click(function(event){
             $.ajax({ 
                type: "DELETE", 
                url: "", 
                dataType: "xml", 
                complete: function(xml){ 
                    window.location.href = "/"; /* back to index */
                },
             });         
           });
       }    
       if ($("#restartbutton").length) {
           $("#restartbutton").click(function(event){
             $.ajax({ 
                type: "DELETE", 
                url: "output", 
                dataType: "xml", 
                complete: function(xml){ 
                    window.location.href = ""; /* refresh */
                },
             });         
           });
       }    
     });    
    </script>
  </head>
</xsl:template>

<xsl:template name="footer">
    <div id="footer" class="box">Powered by <strong>CLAM</strong> - Computational Linguistics Application Mediator<br />by Maarten van Gompel<br /><a href="http://ilk.uvt.nl">Induction of Linguistic Knowledge Research Group</a>, <a href="http://www.uvt.nl">Tilburg University</a></div>
</xsl:template>
<?xml-stylesheet type="text/xsl" href="http://localhost:8080/static/interface.xsl"?>

<xsl:template match="/clam/status">
    <div id="status" class="box">
     <h3>Status</h3>
     <xsl:if test="@errors = 'yes'">
      <div class="error">
            <strong>Error: </strong> <xsl:value-of select="@errormsg"/>
      </div>
     </xsl:if>     
     <xsl:choose>
      <xsl:when test="@code = 0">
        <div class="ready"><xsl:value-of select="@message"/><input id="abortbutton" type="button" value="Abort and delete project" /></div>
      </xsl:when>
      <xsl:when test="@code = 1">
        <div class="running"><xsl:value-of select="@message"/><input id="abortbutton" type="button" value="Abort and delete project" /></div>
      </xsl:when>
      <xsl:when test="@code = 2">
        <div class="done"><xsl:value-of select="@message"/><input id="abortbutton" type="button" value="Cancel and delete project" /><input id="restartbutton" type="button" value="Discard output and restart" /></div>
      </xsl:when>
      <xsl:otherwise>
        <div class="other"><xsl:value-of select="@message"/></div>
      </xsl:otherwise>
     </xsl:choose>
    </div>
</xsl:template>

<xsl:template match="/clam/inputformats">
        <div class="rightbox uploadform">
            <h3>Upload a file from disk</h3>
            <form method="POST" enctype="multipart/form-data" action="upload/">
                <input type="hidden" name="uploadcount" value="1" />
                <table>
                 <tr><td><label for="upload1">Upload file:</label></td><td><input type="file" name="upload1" /></td></tr>
                 <tr><td><label for="uploadformat1">Format:</label></td><td>
                    <select name="uploadformat1">
                    <xsl:for-each select="*">
                        <option><xsl:attribute name="value"><xsl:value-of select="name(.)" /></xsl:attribute><xsl:value-of select="@name" /></option>
                    </xsl:for-each>
                    </select>
                 </td></tr>
                 <tr><td></td><td><input class="uploadbutton" type="submit" value="Upload file" /></td></tr>
                </table>
            </form>
        </div>
        <div class="leftbox uploadform">
            <h3>Submit input from browser</h3>
            <form method="POST" enctype="multipart/form-data" action="upload/">
                <input type="hidden" name="uploadcount" value="1" />
                <table>
                 <tr><td><label for="uploadtext1">Input:</label></td><td><textarea name="uploadtext1"></textarea></td></tr>
                 <tr><td><label for="uploadfilename1">Desired filename:</label></td><td><input name="uploadfilename1" /></td></tr>
                 <tr><td><label for="uploadformat1">Format:</label></td><td>
                    <select name="uploadformat1">
                    <xsl:for-each select="*">
                        <option><xsl:attribute name="value"><xsl:value-of select="name(.)" /></xsl:attribute><xsl:value-of select="@name" /></option>
                    </xsl:for-each>
                    </select>
                 </td></tr>
                 <tr><td></td><td><input class="uploadbutton" type="submit" value="Submit" /></td></tr>
                </table>
            </form>            
        </div>
</xsl:template>

<xsl:template match="/clam/input">
    <div id="input" class="box">
        <h3>Input files</h3>
        <table>
            <xsl:apply-templates select="path" />
        </table>
    </div>
</xsl:template>

<xsl:template match="/clam/output">
    <div id="output" class="box">
        <h3>Output files</h3>
        <p>(Download all as archive: <a href="output/?format=zip">zip</a> | <a href="output/?format=tar.gz">tar.gz</a> | <a href="output/?format=tar.bz2">tar.bz2</a>)</p>
        <table>
            <xsl:apply-templates select="path" />
        </table>
    </div>
</xsl:template>

<xsl:template match="/clam/input/path">
    <tr><th><xsl:value-of select="."/></th><td><xsl:value-of select="@format"/></td><td><xsl:value-of select="@encoding" /></td></tr>
</xsl:template>


<xsl:template match="/clam/output/path">
    <tr>
    <th><a><xsl:attribute name="href">output/<xsl:value-of select="."/></xsl:attribute><xsl:value-of select="."/></a></th>
    <td><xsl:value-of select="@format"/></td><td><xsl:value-of select="@encoding"/></td>
    </tr>
</xsl:template>

<xsl:template match="/clam/parameters">
    <form method="POST" enctype="multipart/form-data" action="">
    <div id="parameters" class="box">
        <h3>Parameter Selection</h3>

        <xsl:for-each select="parametergroup">
         <h4><xsl:value-of select="@name" /></h4>
         <table>
          <xsl:apply-templates />
         </table>
        </xsl:for-each>

        <div id="corpusselection">
        <label for="usecorpus">Input source:</label>
        <select name="usecorpus">
            <option value="" selected="selected">Use uploaded files</option>
            <xsl:for-each select="../corpora/corpus">
                <option><xsl:attribute name="value"><xsl:value-of select="." /></xsl:attribute><xsl:value-of select="." /></option>
            </xsl:for-each>
        </select>
        </div>
        <div id="startbutton">
            <input type="submit" class="start" value="Start" />
        </div>
    </div>
    </form>
</xsl:template>


<xsl:template match="/clamupload">
  <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <xsl:call-template name="head" />
  <body>
    <div id="header"><h1><xsl:value-of select="@name"/></h1><h2><xsl:value-of select="@project"/></h2></div>
    <xsl:for-each select="upload">
        <div id="upload" class="box">
            <a href="../">Return to the project view</a>
            <ul>
              <xsl:apply-templates select="file"/>  
            </ul>
        </div>
    </xsl:for-each>
    <xsl:call-template name="footer" />
  </body>
  </html>
</xsl:template>

<xsl:template match="file">
    <xsl:choose>
    <xsl:when test="@validated = 'yes'">
        <li class="ok"><tt><xsl:value-of select="@name" /></tt>: OK</li>    
    </xsl:when>
    <xsl:otherwise>
        <li class="failed"><tt><xsl:value-of select="@name" /></tt>: Failed</li>    
    </xsl:otherwise>
    </xsl:choose>
</xsl:template>


<xsl:template match="/clamindex">
  <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <xsl:call-template name="head" />
  <body>
    <div id="container">
        <div id="header"><h1><xsl:value-of select="@name"/></h1><h2><xsl:value-of select="@project"/></h2></div>
        <div id="description" class="box">
              <xsl:value-of select="description" />   
        </div>
        <div id="startproject" class="box">
            <h3>Start a new Project</h3>    
                Project ID: <input id="projectname" type="projectname" value="" />
                <input id="startprojectbutton" type="button" value="Start project" />
        </div>
        <div id="index" class="box">
        <h3>Projects</h3>
        <xsl:for-each select="projects/project">
                <ul>
                  <li><a><xsl:attribute name="href"><xsl:value-of select="." />/</xsl:attribute><xsl:value-of select="." /></a></li>
                </ul>
        </xsl:for-each>
        </div>
        <xsl:call-template name="footer" />
    </div>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>