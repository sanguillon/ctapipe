# Connect to the database (here in memory)
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True, echo_pool=True)

# Import sqlachemy modules to create objects mapped with tables
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy import exists
from sqlalchemy.orm import relationship

# Declare a declarative_base to map objets and tables
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

#----------------------------------------------------------------------------------------------------------
# wasInformedBy association table (n-n relation)

wasInformedBy_association_table = Table('wasInformedBy', Base.metadata,
    Column('wasInformedBy_Id', Integer, primary_key=True),
    Column('informant', String, ForeignKey("activities.id")),
    Column('informed', String, ForeignKey("activities.id")))

#----------------------------------------------------------------------------------------------------------
# Define the Activity class mapped to the activities table

class Activity(Base):
    __tablename__ = 'activities'
    ordered_attribute_list = ['id','name','startTime','endTime','comment','activityDescription_id']
    # Key
    id        = Column(String, primary_key=True)
    # Model attributes
    name      = Column(String)
    startTime = Column(String) 
    endTime   = Column(String)
    comment   = Column(String) 

    # n-1 relation with ActivityDescription
    activityDescription_id = Column(String, ForeignKey("activityDescriptions.id"))
    activityDescription    = relationship("ActivityDescription")
    
    # n-n relation with Activity itsself
    #wasInformedBy = relationship('Activity', secondary=wasInformedBy_association_table, 
        #primaryjoin=id == wasInformedBy_association_table.c.informed,
        #secondaryjoin=id == wasInformedBy_association_table.c.informant,
        #backref=backref('informed')
    #    )
    
    # Print method
    def __repr__(self):
        response = ""
        for attribute in self.ordered_attribute_list:
            response += "Activity.%s=%s\n" %(attribute,self.__dict__[attribute])
        return response

#----------------------------------------------------------------------------------------------------------
# wasDerivedFrom association table (n-n relation)

wasDerivedFrom_association_table = Table('wasDerivedFrom', Base.metadata,
    Column('generatedEntity', String, ForeignKey("entities.id")),
    Column('usedEntity', String, ForeignKey("entities.id")))

#----------------------------------------------------------------------------------------------------------
# Define the Entity class mapped to the entities table

class Entity(Base):
    __tablename__ = 'entities'
    ordered_attribute_list = ['id','classType','name','location','generatedAtTime','invalidatedAtTime','comment','classType','entityDescription_id' ]
    
    # Key
    id                  = Column(String, primary_key=True)
    # Model attributes
    name                = Column(String)
    location            = Column(String) 
    generatedAtTime     = Column(String)
    invalidatedAtTime   = Column(String)
    comment             = Column(String)

    # n-1 relation with EntityDescription
    entityDescription_id   = Column(String, ForeignKey("entityDescriptions.id")) 
    entityDescription      = relationship("EntityDescription")
    
    # n-n relation with Entity itsself
    #wasDerivedFrom = relationship('Entity', secondary=wasDerivedFrom_association_table)
    
    # Heritage
    classType           = Column(String)
    __mapper_args__ = {
        'polymorphic_identity':'entity',
        'polymorphic_on': classType
    }
    
    # print method
    def __repr__(self):
        response = ""
        for attribute in self.ordered_attribute_list:
            response += "Entity.%s=%s\n" %(attribute,self.__dict__[attribute])
        return response

#----------------------------------------------------------------------------------------------------------
# Define the Used class mapped to the used table

class Used(Base):
    __tablename__ = 'used'
    ordered_attribute_list = ['id','role','time','activity_id','entity_id', 'usageDescription_id']
    
    # Key
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Model attributes 
    role     = Column(String, nullable=True)
    time     = Column(String)
    
    # n-1 relation with Activity
    activity_id = Column(String, ForeignKey('activities.id'))
    activity = relationship("Activity")
    
    # n-1 relation with Entity
    entity_id = Column(String, ForeignKey('entities.id'))
    entity = relationship("Entity")
    
    # n-0..1 relation with UsageDescription
    usageDescription_id   = Column(String, ForeignKey("usageDescriptions.id")) 
    usageDescription      = relationship("UsageDescription")
    
    # Print method
    def __repr__(self):
        response = ""
        for attribute in self.ordered_attribute_list:
            response += "Used.%s=%s\n" %(attribute,self.__dict__[attribute])
        return response

#----------------------------------------------------------------------------------------------------------
# Define the WasGeneratedBy class mapped to the wasGeneratedBy table

class WasGeneratedBy(Base):
    __tablename__ = 'wasGeneratedBy'
    ordered_attribute_list = ['id','role','activity_id','entity_id', 'generationDescription_id']
    
    # Key
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Model attributes
    role     = Column(String, nullable=True)
    
    # n-1 relation with Activity
    activity_id = Column(String, ForeignKey('activities.id'))
    activity = relationship("Activity")
    
    # 0..1-1 relation with Entity
    entity_id = Column(String, ForeignKey('entities.id'))
    entity = relationship("Entity")
    
    # n-1 relation with GenerationDescription
    generationDescription_id   = Column(String, ForeignKey("generationDescriptions.id")) 
    generationDescription      = relationship("GenerationDescription")
    
    # Print method
    def __repr__(self):
        response = ""
        for attribute in self.ordered_attribute_list:
            response += "WasGeneratedBy.%s=%s\n" %(attribute,self.__dict__[attribute])
        return response

#----------------------------------------------------------------------------------------------------------
# Define the ValueEntity class mapped to the valueEntities table

class ValueEntity(Entity):
    __tablename__ = 'valueEntities'
    ordered_attribute_list = Entity.ordered_attribute_list
    
    # Key
    id = Column(String, ForeignKey('entities.id'), primary_key=True)
    # Model attributes
    value = Column(String)
    
    # Heritage
    __mapper_args__ = {'polymorphic_identity':'value'}
    
    # Print method
    def __repr__(self):
        response = ""
        for attribute in self.ordered_attribute_list:
            response += "ValueEntity.%s=%s\n" %(attribute,self.__dict__[attribute])
        return response

#----------------------------------------------------------------------------------------------------------
# Define the DatasetEntity class mapped to the datasetEntities table

class DatasetEntity(Entity):
    __tablename__ = 'datasetEntities'
    ordered_attribute_list = Entity.ordered_attribute_list
    
    # Key
    id = Column(String, ForeignKey('entities.id'), primary_key=True)
    # Model attributes
    
    # Heritage
    __mapper_args__ = {'polymorphic_identity':'dataset'}
    
    # Print method
    def __repr__(self):
        response = ""
        for attribute in self.ordered_attribute_list:
            response += "DatasetEntity.%s=%s\n" %(attribute,self.__dict__[attribute])
        return response

#----------------------------------------------------------------------------------------------------------
# Define the Agent class mapped to the agents table

class Agent(Base):
    __tablename__ = 'agents'
    ordered_attribute_list = ['id','name','type','email','affiliation','phone','address','comment','url']
    
    # Key
    id                  = Column(String, primary_key=True)
    # Model attributes
    name                = Column(String)
    type                = Column(String) 
    email               = Column(String)
    affiliation         = Column(String)
    phone               = Column(String)
    address             = Column(String)
    comment             = Column(String)
    url                 = Column(String)
    
    # Print method
    def __repr__(self):
        response = ""
        for attribute in self.ordered_attribute_list:
            response += "Agent.%s=%s\n" %(attribute,self.__dict__[attribute])
        return response

#----------------------------------------------------------------------------------------------------------
# Define the WasAssociatedWith class mapped to the wasAssociatedWith table
class WasAssociatedWith(Base):

    __tablename__ = 'wasAssociatedWith'
    ordered_attribute_list = ['id','activity','agent','role']
    
    # Key
    id       = Column(Integer, primary_key=True, autoincrement=True)
    # Model attributes
    role     = Column(String, nullable=True)
    
    # n-1 relation with Activity
    activity = Column(String, ForeignKey("activities.id")) 
    
    # n-1 relation with Agent
    agent    = Column(String, ForeignKey("agents.id")) 
    
    # Print method
    def __repr__(self):
        response = ""
        for attribute in self.ordered_attribute_list:
            response += "WasAssociatedWith.%s=%s\n" %(attribute,self.__dict__[attribute])
        return response

#----------------------------------------------------------------------------------------------------------
# Define the WasAttributedTo class mapped to the wasAttributedTo table

class WasAttributedTo(Base):
    __tablename__ = 'wasAttributedTo'
    ordered_attribute_list = ['id','entity','agent','role']
    
    # Key
    id       = Column(Integer, primary_key=True, autoincrement=True)
    # Model attributes
    role     = Column(String, nullable=True)
    
    # n-1 relation with Entity
    entity   = Column(String, ForeignKey("entities.id")) 
    
    # n-1 relation with Agent
    agent    = Column(String, ForeignKey("agents.id")) 
    
    # Print method
    def __repr__(self):
        response = ""
        for attribute in self.ordered_attribute_list:
            response += "WasAttributedTo.%s=%s\n" %(attribute,self.__dict__[attribute])
        return response

#----------------------------------------------------------------------------------------------------------
# Define the ActivityDescription class mapped to the activityDescriptions table

class ActivityDescription(Base):
    __tablename__ = 'activityDescriptions'
    ordered_attribute_list = ['id','name','version','description','type','subtype','doculink']
    
    # Key
    id                 = Column(String, primary_key=True)
    # Model attributes
    name               = Column(String)
    version            = Column(String)
    description        = Column(String)
    type               = Column(String) 
    subtype            = Column(String)
    doculink           = Column(String)
    
    # Print method
    def __repr__(self):
        response = ""
        for attribute in self.ordered_attribute_list:
            response += "ActivityDescription.%s=%s\n" %(attribute,self.__dict__[attribute])
        return response

#----------------------------------------------------------------------------------------------------------
# Define the EntityDescription class mapped to the entityDescriptions table

class EntityDescription(Base):
    __tablename__ = 'entityDescriptions'
    ordered_attribute_list = ['id','name','type','description','doculink','classType']
    
    # Key
    id                 = Column(String, primary_key=True)
    # Model attributes
    name               = Column(String)
    type               = Column(String)
    description        = Column(String)
    doculink           = Column(String)
    
    # Heritage
    classType          = Column(String)
    __mapper_args__ = {
        'polymorphic_identity':'entityDescription',
        'polymorphic_on':classType
    }
    
    # Print method
    def __repr__(self):
        response = ""
        for attribute in self.ordered_attribute_list:
            response += "EntityDescription.%s=%s\n" %(attribute,self.__dict__[attribute])
        return response

#----------------------------------------------------------------------------------------------------------
# Define the UsageDescription class mapped to the usageDescriptions table
class UsageDescription(Base):

    __tablename__ = 'usageDescriptions'
    ordered_attribute_list = ['id','role','description','type','activityDescription_id','entityDescription_id']
    
    # Key
    id = Column(String, primary_key=True)
    # Model attributes
    role         = Column(String, nullable=True)
    description  = Column(String)
    type         = Column(String) 
    multiplicity = Column(Integer)
    
    # n-1 relation with ActivityDescription 
    activityDescription_id = Column(String, ForeignKey('activityDescriptions.id'))
    activityDescription = relationship("ActivityDescription")
    
    # n-1 relation with EntityDescription 
    entityDescription_id = Column(String, ForeignKey('entityDescriptions.id'))
    entityDescription = relationship("EntityDescription")
    
    # Print method
    def __repr__(self):
        response = ""
        for attribute in self.ordered_attribute_list:
            response += "UsageDescription.%s=%s\n" %(attribute,self.__dict__[attribute])
        return response

#----------------------------------------------------------------------------------------------------------
# Define the GenerationDescription class mapped to the generationDescriptions table

class GenerationDescription(Base):
    __tablename__ = 'generationDescriptions'
    ordered_attribute_list = ['id','role','description','type','activityDescription_id','entityDescription_id']
    
    # Key
    id          = Column(String, primary_key=True)
    # Model attributes
    role         = Column(String, nullable=True)
    description  = Column(String)
    type         = Column(String)
    multiplicity = Column(Integer)
    
    # n-1 relation with ActivityDescription
    activityDescription_id = Column(String, ForeignKey('activityDescriptions.id'))
    activityDescription = relationship("ActivityDescription")
    
    # n-1 relation with EntityDescription
    entityDescription_id = Column(String, ForeignKey('entityDescriptions.id'))
    entityDescription = relationship("EntityDescription")
    
    # Print method
    def __repr__(self):
        response = ""
        for attribute in self.ordered_attribute_list:
            response += "GenerationDescription.%s=%s\n" %(attribute,self.__dict__[attribute])
        return response
    
#----------------------------------------------------------------------------------------------------------
# Define the ValueDescription class mapped to the valueDescriptions table

class ValueDescription(EntityDescription):
    __tablename__ = 'valueDescriptions'
    #ordered_attribute_list = EntityDescription.ordered_attribute_list + ['valueType','unit','ucd','utype','min','max','default','options']
    ordered_attribute_list = EntityDescription.ordered_attribute_list
    
    # Key
    id = Column(String, ForeignKey('entityDescriptions.id'), primary_key=True)
    # Model attributes
    valueType = Column(String)
    unit      = Column(String)
    ucd       = Column(String)
    utype     = Column(String)
    min       = Column(String)
    max       = Column(String)
    default   = Column(String)
    options   = Column(String)
    
    # Heritage
    __mapper_args__ = {'polymorphic_identity':'valueDescription'}
    
    # Print method
    def __repr__(self):
        response = ""
        for attribute in self.ordered_attribute_list:
            response += "ValueDescription.%s=%s\n" %(attribute,self.__dict__[attribute])
        return response

#----------------------------------------------------------------------------------------------------------
# Define the DatasetDescription class mapped to the datasetDescriptions table

class DatasetDescription(EntityDescription):
    __tablename__ = 'datasetDescriptions'
    #ordered_attribute_list = EntityDescription.ordered_attribute_list + ['contentType']
    ordered_attribute_list = EntityDescription.ordered_attribute_list
    
    # Key
    id = Column(String, ForeignKey('entityDescriptions.id'), primary_key=True)
    # Model attributes
    contentType = Column(String)
    
    # Heritage
    __mapper_args__ = {'polymorphic_identity':'datasetDescription'}
    
    # Print method
    def __repr__(self):
        response = ""
        for attribute in self.ordered_attribute_list:
            response += "DatasetDescription.%s=%s\n" %(attribute,self.__dict__[attribute])
        return response

#----------------------------------------------------------------------------------------------------------
# Define the Parameter class mapped to the parameters table

class Parameter(Base):
    __tablename__ = 'parameters'
    ordered_attribute_list = ['id', 'value', 'name', 'parameterDescription_id']
    
    # Key
    id    = Column(String, ForeignKey('valueEntities.id'), primary_key=True)
    # Model attributes
    value = Column(String)
    name  = Column(String)
    
    # n-0..1 relation with ParameterDescription
    parameterDescription_id   = Column(String, ForeignKey("parameterDescriptions.id")) 
    parameterDescription      = relationship("ParameterDescription")
    
    # n-0..1 relation with ValueEntity
    valueEntity      = relationship("ValueEntity")
    
    # Print method
    def __repr__(self):
        response = ""
        for attribute in self.ordered_attribute_list:
            response += "Parameter.%s=%s\n" %(attribute,self.__dict__[attribute])
        return response

#----------------------------------------------------------------------------------------------------------
# Define the ParameterDescription class mapped to the parameterDescriptions table

class ParameterDescription(Base):
    __tablename__ = 'parameterDescriptions'
    ordered_attribute_list = ['id','name','valueType','unit','ucd','utype','min','max','default','options','description']
    
    # Key
    id = Column(String, ForeignKey('valueDescriptions.id'), primary_key=True)
    # Model attributes
    name        = Column(String)
    valueType   = Column(String)
    unit        = Column(String)
    ucd         = Column(String)
    utype       = Column(String)
    min         = Column(String)
    max         = Column(String)
    options     = Column(String)
    default     = Column(String)
    description = Column(String)
    
    # Print method
    def __repr__(self):
        response = ""
        for attribute in self.ordered_attribute_list:
            response += "ParameterDescription.%s=%s\n" %(attribute,self.__dict__[attribute])
        return response
        
#----------------------------------------------------------------------------------------------------------
# Define the ConfigFile class mapped to the configFiles table

class ConfigFile(Base):
    __tablename__ = 'configFiles'
    ordered_attribute_list = ['id', 'name', 'location', 'comment', 'configFileDescription_id']
    
    # Key
    id    = Column(String, ForeignKey('valueEntities.id'), primary_key=True)
    # Model attributes
    name     = Column(String)
    location = Column(String)
    comment  = Column(String)
    
    # 1-n relation with ConfigFileDescription 
    configFileDescription_id = Column(String, ForeignKey('configFileDescriptions.id'))
    configFileDescription = relationship("ConfigFileDescription")
    
    # 1-n relation with ParameterDescription 
    parameterDescription_id = Column(String, ForeignKey('parameterDescriptions.id'))
    parameterDescription = relationship("ParameterDescription")
    
    # Print method
    def __repr__(self):
        response = ""
        for attribute in self.ordered_attribute_list:
            response += "Parameter.%s=%s\n" %(attribute,self.__dict__[attribute])
        return response

#----------------------------------------------------------------------------------------------------------
# Define the ParameterDescription class mapped to the parameterDescriptions table

class ConfigFileDescription(Base):
    __tablename__ = 'configFileDescriptions'
    ordered_attribute_list = ['id','name','contextType','description']
    
    # Key
    id = Column(String, ForeignKey('valueDescriptions.id'), primary_key=True)
    # Model attributes
    name        = Column(String)
    contextType = Column(String)
    description = Column(String)
    
    
    # Print method
    def __repr__(self):
        response = ""
        for attribute in self.ordered_attribute_list:
            response += "ParameterDescription.%s=%s\n" %(attribute,self.__dict__[attribute])
        return response


#----------------------------------------------------------------------------------------------------------
# Define the WasConfiguredBy class mapped to the used table

class WasConfiguredBy(Base):
    __tablename__ = 'wasConfiguredBy'
    ordered_attribute_list = ['id','artefactType','activity_id','parameter_id']
    
    # Key
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Model attributes
    artefactType     = Column(String, nullable=True)
    
    # n-1 relation with Activity
    activity_id = Column(String, ForeignKey('activities.id'))
    activity = relationship("Activity")
    
    # 1-0..1 relation with Parameter
    parameter_id = Column(String, ForeignKey('parameters.id'))
    parameter = relationship("Parameter")
    
    # 1-0..1 relation with ConfigFile
    configFile_id = Column(String, ForeignKey('configFiles.id'))
    configFile = relationship("ConfigFile")
    
    # Print method
    def __repr__(self):
        response = ""
        for attribute in self.ordered_attribute_list:
            response += "WasConfiguredBy.%s=%s\n" %(attribute,self.__dict__[attribute])
        return response
        
#----------------------------------------------------------------------------------------------------------
# sqlalchemy creates the database for me
Base.metadata.create_all(engine)

