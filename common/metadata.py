###############################################################
# CLAM: Computational Linguistics Application Mediator
# -- Metadata and profiling --
#       by Maarten van Gompel (proycon)
#       http://ilk.uvt.nl/~mvgompel
#       Induction for Linguistic Knowledge Research Group
#       Universiteit van Tilburg
#       
#       Licensed under GPLv3
#
##############################################################


import json
from lxml import etree as ElementTree

def profiler(inputfiles,parameters):
    """Given input files and parameters, produce metadata for outputfiles. Returns list of matched profiles if succesfull, empty list otherwise"""
    matched = []
    for profile in PROFILES:
        if profile.match(inputfiles, parameters):
            matched.append(profile)
            profile.generate(inputfiles,parameters)
    return matched


class Profile(object):
    def __init__(self, input, output, parameters, **kwargs):
        if not isinstance(input, list):
            input = [input]
        if isinstance(input, InputTemplate):
           assert all([ isinstance(InputTemplate) for x in input])
        self.input = input

        if isinstance(output, OutputTemplate) or isinstance(output, ParameterCondition):
            output = [output]
        assert all([ isinstance(OutputTemplate) or isinstance(ParameterCondition)  for x in output])
        self.output = output

        self.multi = False

        for key, value in kwargs.items():
            if key == 'unique':
                self.multi = not value
            elif key == 'multi':
                self.multi = value
            else:
                raise SyntaxError("Unknown parameter to profile: " + key)

    def match(self, inputfiles, parameters):
        """Check if the profile matches inputdata *and* produces output given the set parameters. Return boolean"""

        #check if profile matches inputdata
        for inputtemplate in self.input:
            if not inputtemplate.match(inputfiles):
                return False

        #check if output is produced
        match = False
        for outputtemplate in self.output:
            if outputtemplate.match(parameters):
                match = True
        return match


    def generate(self, inputfiles, parameters):
        """Generate output metadata on the basis of input files and parameters"""
        raise NotImplementedError #TODO: implement

        if self.match(self, inputfiles, parameters):

            #loop over inputfiles
            #   see if inputfile matches inputtemplates
            #    see if any outputtemplates become active (may be parameter dependent)
            #     generate outputmetadata based on outputtemplats

            #TODO !!!!!!

            for inputfile in inputfiles:
                #load inputfile metadata
                


            for outputtemplate in self.output:
                if isinstance(outputtemplate, ParameterCondition):
                    outputtemplate = outputtemplate.evaluate(parameters)
                if outputtemplate and outputtemplate.match(parameters):
                    outputtemplate.generate(inputdata, parameters)

    def xml(self):
        """Produce XML output for the profile""" #(independent of web.py for support in CLAM API)
        xml = "<profile"
        if self.multi:
            xml += "  multi=\"yes\""
        else:   
            xml += "  multi=\"no\""
        xml += ">\n<input>\n"
        for inputtemplate in self.input:
            xml += inputtemplate.xml()
        xml += "</input>\n"
        xml += "<output>\n"
        for outputtemplate in self.input:
            xml += outputtemplate.xml() #works for ParameterCondition as well!
        xml += "<output>\n"
        xml += "</profile>\n"
        return xml
        


class IncompleteError(Exception):
    pass



def getmetadata(xmldata):
    """Read metadata from XML"""
    raise NotImplementedError #TODO: implement

class CLAMMetaData(object):
    """A simple hash structure to hold arbitrary metadata"""
    attributes = None #if None, all attributes are allowed! Otherwise it should be a dictionary with keys corresponding to the various attributes and a list of values corresponding to the *maximally* possible settings (include False as element if not setting the attribute is valid), if no list of values are defined, set True if the attrbute is required or False if not. If only one value is specified (either in a list or not), then it will be 'fixed' metadata

    mimetype = "" #No mimetype by default
    schema = ""
    
    self.input = False
    self.output = False

    def __init__(self, **kwargs):
        self.data = {}
        for key, value in kwargs.items():
            if key == 'origin': #TODO: add origin
                self.input = True
                self.systemid, self.systemname, self.systemurl, self.project, self.templateid,self.templatelabel = value
            else:
                self[key] = value
        if attributes:
            if not allowcustomattributes:
                for key, value in kwargs.items():
                    if not key in attributes:
                        raise ValueError("Invalid attribute '" + key + " specified. But this format does not allow custom attributes.")
                            
            
            for key, valuerange in attributes.items():
                if isinstance(valuerange,list):
                    if not key in self and not False in valuerange :
                        raise ValueError("Required attribute " + key +  " not specified")
                    elif self[key] not in valuerange:
                        raise ValueError("Attribute assignment " + key +  "=" + self[key] + " has an invalid value, choose one of: " + " ".join(attributes[key])
                elif valuerange is False: #Any value is allowed, and this attribute is not required
                    pass #nothing to do
                elif valuerange is True: #Any value is allowed, this attribute is *required*    
                    if not key in self:
                        raise IncompleteError("Required attribute " + key +  " not specified")
                elif valuerange: #value is a single specific unconfigurable value 
                    self[key] = valuerange

    def __getitem__(self, key):
        return self.data[key]

    def __contains__(self, key)
        return key in self.data

    def items(self):
        return self.data.items()

    def __iter__(self):
        return self.data

    def __setitem__(self, key, value):
        if attributes != None and not key in attributes:
            raise KeyError
        assert not isinstance(value, list)
        maxvalues = self.data[key]
        if isinstance(maxvalues, list):
            if not value in maxvalues:
                raise ValueError
        self.data[key] = value


    def xml(self):
        """Render an XML representation of the metadata""" #(independent of web.py for support in CLAM API)
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += "<CLAMMetaData format=\"" + self.__class__.__name__ + "\"
        if self.mimetype:
             xml += " mimetype=\""+self.__class__.mimetype+"\""
        if self.schema:
             xml += " schema=\""+self.__class__.schema+"\""
        xml += ">\n"
        
        #TODO: Add origin path
        #xml += "\t<origin>"
        #xml += "\t\t<clamservice systemid=\""+ self.systemid +"\" systemname=\""+ self.systemname + "\" systemurl=\""+ self.systemurl +"\"   template=\""+ template.id +"\" label=\""+template.label+"\">"
        #xml += "\t\t" + self.origin.metadata.xml()
        #xml += "\t\t</clamservice>"
        #xml += "\t</origin>"    
            
        for key, value in self.data.items():
        xml += "\t<meta id=\""+key+"\">"+str(value)+"</meta>"
        
        xml += "</CLAMMetaData>"
        return xml

    def save(self, filename):
        f = codecs.open(filename,'w','utf-8')
        f.write(self.xml())
        f.close()

class CMDIMetaData(CLAMMetaData):
    #TODO LATER: implement



def profilefromxml():
    """Produce profile from xml"""
    raise NotImplementedError #TODO: implement
    

class InputTemplate(object):
    def __init__(self, id, formatclass, label, *args, **kwargs)
        assert (issubclass(formatclass, CLAMMetaData))
        assert (not '/' in id and not '.' in id)
        self.formatclass = formatclass
        self.id = id
        self.label = label

        self.parameters = []
        
        self.unique = True #may mark input/output as unique, even though profile may be in multi mode

        self.filename = None
        self.extension = None

        for key, value in kwargs.items():
            if key == 'unique':   
                self.unique = bool(value)
            elif key == 'multi':   
                self.unique = not bool(value)
            elif key == 'filename':
                self.filename = value # use '#' to insert a number in multi mode (will happen server-side!)
            elif key == 'extension':
                self.extension = value

        if not self.unique and not '#' in self.filename:
            raise Exception("InputTemplate configuration error, filename is set to a single specific name, but unique is disabled. Use '#' in filename, which will automatically resolve to a number in sequence.")

        for parameter in args:
            assert isinstance(parameter, AbstractParameter)
            self.parameters.append(parameter)


    def xml(self):
        """Produce Template XML"""
        xml = "<InputTemplate format=\"" + self.formatclass.__name__ + "\"" + " label=\"" + self.label + "\""
        if self.formatclass.mimetype:
            xml +=" mimetype=\""+self.formatclass.mimetype+"\""
        if self.formatclass.schema:
            xml +=" schema=\""+self.formatclass.schema+"\""
        if self.filename:
            xml +=" filename=\""+self.filename+"\""
        if self.extension:
            xml +=" extension=\""+self.extension+"\""
        if self.unique:
            xml +=" unique=\"yes\""
        xml += ">\n"
        for parameter in self.parameters:
            xml += parameter.xml()
        xml += "</InputTemplate>\n"
        return xml

            
    def json(self):
        """Produce a JSON representation for the web interface"""
        d = { 'id': self.id, 'format': self.formatclass.__name__,'label': self.label, 'mimetype': self.formatclass.mimetype,  'schema': self.formatclass.schema }
        if self.unique:
            d['unique'] = True
        if self.filename:
            d['filename'] = self.filename
        if self.extension:
            d['extension'] = self.extension
        #d['parameters'] = {}

        #The actual parameters are included as XML, and transformed by clam.js using XSLT (parameter.xsl) to generate the forms
        parametersxml = ''
        for parameter in self.parameters:
            #d['parameters'][parameter.id] = parameter.json()
            parameterxml = parameter.xml()
        d['parametersxml'] = parameterxml
        return json.dumps(d)

    def __eq__(self, other):
        return other.id == self.id

    def match(self, metadata, user = None):
        """Does the specified metadata match this template? returns (success,metadata,parameters)"""
        assert isinstance(metadata, self.formatclass)
        return self.generate(metadata,user)

    def generate(self, inputdata, user = None):
        """Convert the template into instantiated metadata, validating the data in the process and returning errors otherwise. inputdata is a dictionary-compatible structure, such as the relevant postdata. Return (success, metadata, parameters), error messages can be extracted from parameters[].error"""
        
        metadata = self.formatclass()
        errors = []
        
        #we're going to modify parameter values, this we can't do
        #on the inputtemplate variable, that won't be thread-safe, we first
        #make a (shallow) copy and act on that          
        for parameter in self.parameters:
            parameters.append(copy(parameter))
        
        
        for parameter in parameters:
            if parameter.access(user):
                postvalue = parameter.valuefrompostdata(postdata) #parameter.id in postdata and postdata[parameter.id] != '':    
                if not (isinstance(postvalue,bool) and postvalue == False):
                    if parameter.set(postvalue): #may generate an error in parameter.error
                        params.append(parameter.compilearg(parameter.value))
                    else:
                        if not parameter.error: parameter.error = "Something mysterious went wrong whilst settings this parameter!" #shouldn't happen
                        printlog("Unable to set " + parameter.id + ": " + parameter.error)
                        errors = True
                elif parameter.required:
                    #Not all required parameters were filled!
                    parameter.error = "This option must be set"
                    errors = True
                if parameter.value and (parameter.forbid or parameter.require):
                    for parameter2 in parameters:
                            if parameter.forbid and parameter2.id in parameter.forbid and parameter2.value:
                                parameter.error = parameter2.error = "Setting parameter '" + parameter.name + "' together with '" + parameter2.name + "'  is forbidden"
                                printlog("Setting " + parameter.id + " and " + parameter2.id + "' together is forbidden")
                                errors = True
                            if parameter.require and parameter2.id in parameter.require and not parameter2.value:
                                parameter.error = parameter2.error = "Parameters '" + parameter.name + "' has to be set with '" + parameter2.name + "'  is"
                                printlog("Setting " + parameter.id + " requires you also set " + parameter2.id )
                                errors = True
        
        #scan errors and set metadata
        success = True
        for parameter in parameters:
            if parameter.error:
                success = False
            else:
                metadata[parameter.id] = parameter.value
 
        if not success:
            metadata = None
            
        return success, metadata, parameters
    
        


class OutputTemplate(object):
    def __init__(self, id, formatclass, label, *args, **kwargs)
        assert (issubclass(formatclass, CLAMMetaData))
        assert (not '/' in id and not '.' in id)
        self.id = id
        self.formatclass = formatclass
        self.label = label

        self.metafields = []
        
        self.unique = True #may mark input/output as unique, even though profile may be in multi mode

        self.filename = None
        self.extension = None

        for key, value in kwargs.items():
            if key == 'unique':
                self.unique = bool(value)
            elif key == 'multi':
                self.unique = not bool(value)
            elif key == 'filename':
                self.filename = value # use $N to insert a number in multi mode
            elif key == 'extension':
                self.extension = value

        if not self.unique and not '#' in self.filename:
            raise Exception("OutputTemplate configuration error, filename is set to a single specific name, but unique is disabled. Use '#' in filename, which will automatically resolve to a number in sequence.")

        for metafield in args:
            #TODO
            self.metafields()

    def xml(self):
        """Produce Template XML"""
        xml = "<OutputTemplate format=\"" + self.formatclass.__name__ + "\"" + " label=\"" + self.label + "\""
        if self.formatclass.mimetype:
            xml +=" mimetype=\""+self.formatclass.mimetype+"\""
        if self.formatclass.schema:
            xml +=" schema=\""+self.formatclass.schema+"\""
        if self.unique:
            xml +=" unique=\"yes\""
        xml += ">\n"

        xml += "</OutputTemplate>\n"
        return xml


    def __eq__(self, other):
        return other.id == self.id

    def match(self, parameters):
        #TODO

    def json(self):
        #TODO

    def generate(self):
        #TODO


def ParameterCondition(object):
    def __init__(self, **kwargs):
        if not 'then' in kwargs:
            assert Exception("No 'then=' specified!")

        self.then = None
        self.otherwise = None

        self.conditions = []
        self.disjunction = False

        for key, value in kwargs.items():
            if key == 'then'
                if not isinstance(value, OutputTemplate) and not isinstance(value, InputTemplate) and not isinstance(value, ParameterCondition):
                    assert Exception("Value of 'then=' must be InputTemplate, OutputTemplate or ParameterCondition!")
                else:
                    self.then = value
            elif key == 'else' or key == 'otherwise':
                if not isinstance(value, OutputTemplate) and not isinstance(value, InputTemplate) and not isinstance(value, ParameterCondition):
                    assert Exception("Value of 'else=' must be InputTemplate, OutputTemplate or ParameterCondition!")
                else:
                    self.otherwise = value
            elif key == 'disjunction' or key == 'or':
                self.disjunction = value
            else:
                if key[-10:] == '_notequals':
                    self.conditions.append( (key[:-10], value,lambda x: x != value, 'notequals') )
                elif key[-12:] == '_greaterthan':
                    self.conditions.append( (key[:-12], value,lambda x: x > value, 'greaterthan') )
                elif key[-17:] == '_greaterequalthan':
                    self.conditions.append( (key[:-17],value, lambda x: x > value, 'greaterequalthan') )
                elif key[-9:] == '_lessthan':
                    self.conditions.append( (key[:-9],value, lambda x: x >= value , 'lessthan' ) )
                elif key[-14:] == '_lessequalthan':
                    self.conditions.append( (key[:-14], value,lambda x: x <= value, 'lessequalthan') )
                elif key[-9:] == '_contains':
                    self.conditions.append( (key[:-9], value,lambda x: x in value, 'contains') )
                elif key[-7:] == '_equals':
                    self.conditions.append( (key[:-7], value,lambda x: x == value, 'equals') )
                else: #default is _is
                    self.conditions.append( (key,value, lambda x: x == value,'equals') )
                    

    def match(self, parameters):
        for key,_,evalf,_ in self.conditions:
            if key in parameters:
                value = parameters[key]
            else:
                value = None
            if evalf(value):
                if self.disjunction:
                    return True
            else:
                if not self.disjunction: #conjunction
                    return False
         if self.disjunction:
             return False
         else:
             return True

    def evaluate(self, parameters):
        #Returns False or whatever it evaluates to 
        if self.match(parameters):
            if isinstance(self.then, ParameterCondition):
                #recursive parametercondition
                return self.then.evaluate()
            else:
                return self.then
        elif self.otherwise:
            if isinstance(self.otherwise, ParameterCondition):
                #recursive else
                return self.otherwise.evaluate()
            else:
                return self.otherwise
        return False

    def xml(self):
        xml = "<parametercondition>\n\t<if>\n"
        for key, value, evalf, operator in self.conditions:
            xml += "\t\t<" + operator + " parameter=\"" + key + "\">" + value + "</" + operator + ">"
        xml += "\t</if>\n\t<then>\n"
        xml += self.then.xml() #TODO LATER: add pretty indentation 
        xml += "\t</then>\n"
        if self.otherwise:
            xml += "\t<else>\n"
            xml += self.otherwise.xml() #TODO LATER: add pretty indentation 
            xml += "\t</else>"
        xml += "</parametercondition>"
        return xml








