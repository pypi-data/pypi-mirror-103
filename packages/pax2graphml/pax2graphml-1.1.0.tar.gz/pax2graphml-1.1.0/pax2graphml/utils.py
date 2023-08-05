"""This module contains utilitary functions related to graph and file manipulation, package management and execution."""


__license__ = "MIT"
__docformat__ = 'reStructuredText'


import sys,os
import logging
from decimal import Decimal
from subprocrunner import SubprocessRunner
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import graph_tool.all as gt
import graph_tool.centrality as centrality
import pandas as pd
import argparse
from os import path
import logging
import xml
import tempfile, shutil
import lxml.etree as et

from xml.sax.saxutils import escape
import colorsys

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def resource_path():
    """return the resources  path

        :return:  a string representing the resource \
        path containing additional files like template and  jar
 
    """


    pa = __relPath('resources')

    logger.info("resource_path:%s" % (pa))
    return pa

def data_path():
    """return the data folder  path with example datasets

        :return:  a string representing the data folder \
        path  containing example data files like BIOPAX
 
    """
    pa = __relPath('data')
    logger.info("data_path:%s" % (pa))
    return pa





def node_list(g ):
    """return a  simple  list of all nodes of a graph (without iterator)

        :return:  a list of nodes
 
    """    
    ar=list()
    for el in g.vertices():  
        ar.append(el)

    return ar


def edge_list( g ):

    """return a  simple  list of all edges of a graph (without iterator)

       :return:  a list of edges
 
    """    
    ar=list()
    for el in g.edges():  
        ar.append(el)
 
    return ar 

 


def node_to_string(gh, n, sep="\n"):

    """return a string representing all the properties values from a node

        :return:  a string
    """ 
    s=""  
    for prop in gh.vertex_properties.keys():
        s=s+str(prop)+"="+str(gh.vp[prop][n])+sep
    return s


def to_string(gh, n, sep="\n"):
  """alias of node_to_string

     :return:  a string
  """  
  return node_to_string(gh, n, sep )


def edge_to_string(gh, e, sep="\n"):

    """return a string representing all the properties values from an edge

        :return:  a string
    """ 
    s=""
    for prop in gh.edge_properties.keys():
        s=s+str(prop)+"="+str(gh.ep[prop][e])+sep
    return s


def edge_description(g,e):

    """return a string giving al details from an edge, incuding source an target description

        :return:  a string
    """ 
    ep=edge_to_string(g,e,',')
    sp=node_to_string(g,e.source(),',')
    tp=node_to_string(g,e.target(),',')   
    
    return "edge:%s \n\tsource: %s  \n\ttarget: %s"%(ep,sp,tp)

                        




 
def count_edge(n,mode="all"):

        """compute edges count from a selected node

        :param n: graph node
        :param mode: count mode. values :"all","in", "out"
        :return:  the edges count
        :rtype: int 
        """ 
        ect=0
        if mode=="all":
          for e in n.neighbors():
            ect+=1
        if mode=="in":
          for e in n.in_neighbors():
            ect+=1
        if mode=="out":
          for e in n.out_neighbors():
            ect+=1

        return ect




def cc_by_node_count(g,min,max):

        """select a sub graph from a graph, using the minimum and maximum node number
           of each connected component as as a filter

        :param g: a graph 
        :param min: minimum node count of each connected component
        :param max: maximum node count of each connected component
        :return:  a subgraph
        :rtype: graph 
        """ 

        mccid=dict()
        v2cc = g.new_vertex_property('int');
        ccomp, hist  = gt.label_components(g, directed=None, attractors=False)

        for v in g.vertices():
           ccid=ccomp[v]
           ccidct=0
           if ccid in mccid.keys():
               ccidct=mccid[ccid]

           ccidct+=1
           mccid[ccid]=ccidct
           v2cc[v]=ccid

         
        selectedccid=None
        for ccid in mccid.keys():
             ccidct=  mccid[ccid]
             logging.info("cc id:%s=>%s nodes" %(ccid,ccidct))
             if ccidct>=min and ccidct<=max:
                logging.info("cc id:%s=>%s nodes %s %s " %(ccid,ccidct,min,max))
                selectedccid=ccid
                break
        if selectedccid is not None:
          vfilter = g.new_vertex_property("bool");
          for v in g.vertices():
             cval=v2cc[v]
             vindex=g.vertex_index[v]
             if cval is not None and cval==selectedccid:
                 vfilter[vindex] = True

             else:
                 vfilter[vindex] = False


          u = gt.GraphView(g, vfilt=vfilter)
          u=gt.Graph(u, prune=True)
          return u
        else:
          logger.info("cc_by_node_count returns None" )
          return None 








def friendly_format_graphml(graphml_file,usetemp=False):

      """modify in place a graphml_file to have more human readable properties data key

        :param graphml_file: a graphml file file folling the graph.tools generation rules
      """ 
       
      if usetemp==True: 
        f = tempfile.NamedTemporaryFile(delete=False)
        tmpf=f.name
        #warning: issue with cross devide link
      else:
        tmpf=graphml_file+".work.tmp"


      gns='http://graphml.graphdrawing.org/xmlns'
      ns={'x': gns}
         
 
      root = et.parse(graphml_file)
       
      lst=root.xpath("./x:key", namespaces=ns)
 
      
      keymap=dict()
      for el in lst: 
 
          fv=el.get('for')
          iv=el.get('id')
          v=el.get('attr.name')
          k="%s@%s" %(fv,iv)
          keymap[k]=v
          el.set('id', v)
          
      
      for tag in ["node","edge"]:    
        lst=root.xpath("./x:graph/x:%s" %(tag) , namespaces=ns)
        for elm in lst :   
         for el in elm: 
           
           if el.tag=='{%s}data' %(gns):
            
               ktag="key"
               kv=el.get(ktag)
               k="%s@%s" %(tag,kv)
               v=keymap[k]
               el.set(ktag, v)
 

      idv=0
      lst=root.xpath("./x:graph/x:edge"   , namespaces=ns)
      for el in lst: 
          idv=idv+1
          el.set("id", str(+idv))


           
      root.write(tmpf,
                 pretty_print=True, xml_declaration=True,
                 encoding='UTF-8')

      shutil.move(tmpf, graphml_file)  



 
__P2GJAR="biopax2spaimgen.jar"
__P2GTEMPLATE="graphml.vm"
__P2GJMEM=" -Xmx48g  -XX:+UseConcMarkSweepGC  "
__P2GJVM="java" 

def __gdirEnv():
   """ return the value of an optional evironment variable for alternate resources directory definition""" 
   p2gjdir=os.getenv("P2GJDIR")
   if p2gjdir is None:
      p2gjdir="./"
   return p2gjdir

def __gdir():
   """ return the resources directory if exists else use an evironment variable """ 
   fname=resource_path()
   if (os.path.isdir(fname) ):
      return fname
   else:
      return __gdirEnv()


def __p2g():
    """ paxx2graphml java extension jar name """ 
    return __P2GJAR


def __template():
    """ path to the graphml template used to generate  reaction graph file from BIOPAX.
       this editable template is  processed by the velocity template engine.
       see http://velocity.apache.org
    """ 
    return __gdir()+"/"+__P2GTEMPLATE

def __jarpath():
    """ path to the jar containing the paxx2graphml java extension using paxtools""" 
    return __gdir()+"/"+__p2g()

def __jvm():
    """ java binary """ 
    return __P2GJVM

def __jvmopt():
    """ jvm option """ 
    mem=os.getenv("JVMMEM")
    if mem is None:
       mem=__P2GJMEM
    return mem


def __formatRes(st):
  """utility to find json data in a stdout  string""" 
  ct=""
  fd=0
  ln=st.split("\n")
  for l in ln:
    if l.startswith("{"):
      fd=1
    if fd==1:
      ct+=l

  return ct   

def __runCmd(cmd):
    """command line execution that expect a json output with a status code

        :param cmd: a command line
        :type cmd: string 
        :return:  the json command output
        :rtype: dict 
    """ 
    resp =None
    try:
      runner = SubprocessRunner(cmd)
      logging.info("command: {:s}".format(runner.command))
      logging.info("return code: {:d}".format(runner.run()))
      logging.info("stdout: {:s}".format(runner.stdout))
      logging.info("stderr: {:s}".format(runner.stderr))
      rs=__formatRes(runner.stdout)
      resp = json.loads(rs)
      if resp["status"] ==0:
          logging.info("%s" %(resp["message"]))
      else:
          logging.info("%s" %(resp["error"]))
    except:
        print("error occured! %s %s ." %(sys.exc_info()[0],sys.exc_info()[1]))
    return resp

def __relPath(relname):
    """utility to convert a relative path to current script, to an absolute path  """ 
    resDir = path.join(path.dirname(__file__), relname)
    return resDir


def __addArrayEl(mp,k,el):
    """utility to add element to an array representing the value of a dictionary key""" 
    if k in mp:
      ar=mp[k]
    else:
      ar=list()  
    ar.append(el)
    mp[k]=ar   


def __clean_rm(file):
  err=0
  try:
     shutil.rmtree(graphmlOutFile, False,  None)
  except: 
     err=1 


def __str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def __convertType(v,property_type):
 if property_type is None:
   return v 
 elif property_type=='int':
   v=int(v)
 elif property_type=='float':
   v=float(v)
 elif property_type=='double':
   v=Decimal(v)    
 elif property_type=='double':     
   v=__str2bool(v)
 return v





    
    
def __yed_edge_graphics(label,color):

    """edge graphics for yEd
        :param  label:  node text label
        
        
    """ 
    nstr1='''
            <data key="d27"   xmlns:y="http://www.yworks.com/xml/graphml" >
        <y:PolyLineEdge>
          <y:Path sx="0.0" sy="0.0" tx="0.0" ty="0.0"/>
          <y:LineStyle 
    '''
   
    nstr11='''  
      type="line" width="1.0"/>
          <y:Arrows source="none" target="white_delta"/>
          <y:EdgeLabel alignment="center" configuration="AutoFlippingLabel" distance="2.0" 
          fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" 
           hasLineColor="false" height="17.96875" modelName="custom" 
            preferredPlacement="anywhere" ratio="0.5" textColor="#000000" 
             visible="true" width="53.32421875" x="-71.4431481625477" 
              y="-16.37365500299495">
 
    '''
    nstr2=''' <y:LabelModel>
              <y:SmartEdgeLabelModel autoRotationEnabled="false" defaultAngle="0.0"
              defaultDistance="10.0"/>
            </y:LabelModel>
            <y:ModelParameter>
              <y:SmartEdgeLabelModelParameter angle="0.0" distance="30.0" 
              distanceToCenter="true" position="right" ratio="0.5" segment="0"/>
            </y:ModelParameter>
            <y:PreferredPlacementDescriptor angle="0.0" 
            angleOffsetOnRightSide="0" angleReference="absolute" 
            angleRotationOnRightSide="co" distance="-1.0" frozen="true" 
            placement="anywhere" side="anywhere" sideReference="relative_to_edge_flow"/>
          </y:EdgeLabel>
          <y:BendStyle smoothed="false"/>
        </y:PolyLineEdge>
      </data>
    
    '''
    nscolor=" color=\""+color+"\"  "
    st= nstr1+nscolor+nstr11+label+nstr2
    return st

    
    
def __yed_node_graphics(label,color,shape):

    """node graphics for yEd
        :param  label:  node text label
        
        
    """ 
    nstr1='''
      <data key="d21"   xmlns:y="http://www.yworks.com/xml/graphml" >
        <y:ShapeNode>
          <y:Geometry height="30.0" width="30.0" x="621.3832419501406" y="131.52884981905322"/>
          <y:Fill 
    '''
   
    nstr11=''' transparent="false"/>
          <y:BorderStyle color="#000000" type="line" width="1.0"/>
          <y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog"
           fontSize="12" fontStyle="plain" hasBackgroundColor="false" 
             hasLineColor="false" height="17.96875" modelName="custom" 
             textColor="#000000" visible="true" width="32.998046875" 
             x="-1.4990234375" y="6.015625">
    '''
    nstr2='''
             <y:LabelModel>
              <y:SmartNodeLabelModel distance="4.0"/>
            </y:LabelModel>
            <y:ModelParameter>
              <y:SmartNodeLabelModelParameter labelRatioX="0.0" labelRatioY="0.0"
              nodeRatioX="0.0" nodeRatioY="0.0" offsetX="0.0" offsetY="0.0" upX="0.0" upY="-1.0"/>
            </y:ModelParameter>
          </y:NodeLabel>
          <y:Shape 
    '''
    
    nstr3='''    </y:ShapeNode>
      </data>
    
    '''
    nscolor=" color=\""+color+"\"  "
    nsshape="type=\""+shape+"\"/>"
    st= nstr1+nscolor+nstr11+label+nstr2+nsshape+nstr3
    return st
def spaim_edge_label(code):
    """convert spaim code as defined in spaim edge property to human readable labels 
    """ 
    map_values={
        "s":"is_substrat_of",
        "p":"as_product",
        "a":"is_activator_of",
        "i":"is_inhibitor_of",
        "m":"is_modulator_of",
        
    }
    if code in map_values.keys():
        return map_values[code]
    else:
        return ""

def __node_shape_yed(code):
    """convert biopax type numeric code  as defined in shape node property to yEd compatible shape name
    """ 
    map_values={
   "0": "ellipse",
   "1": "rectangle",
   "2": "octagon",
   "3": "triangle",
   "4": "parallelogram",
   "5": "hexagon",
   "6": "rectangle",
   "7": "diamond",
   "8": "trapezoid"
   }
    if code in map_values.keys():
        return map_values[code]
    else:
        return "trapezoid"

def color_range_hexa(color_number=20):

    hsv = [(x * 1.0 / color_number, 0.8, 0.8) for x in range(color_number)]
    hexout = []
    for color in hsv:
        rgb = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(*color))
        hexout.append('#%02x%02x%02x' % tuple(rgb))
    return hexout

def __color_range():
    map_values={
    "0": "",
    "1": "",
    "2": "",
    "3": "",
    "4": "",
    "5": "",
    "6": "",
    "7": "",
    "8": ""
    }
    sz=len(map_values.keys())
    colors=color_range_hexa(sz)
    
    i=0
    for k in map_values.keys():
        map_values[k]=colors[i]
        i=i+1
    #print(map_values)  
    return map_values

    
def node_shape_to_color(code,colors):
    """convert biopax type numeric code  as defined in shape node property to yEd compatible shape name
    """ 
    
    if code in colors.keys():
        return colors[code]
    else:
        return "#FFFFFF"
   

    
def __format_graphml_yed(graphml_file,usetemp=False):

      """modify in place a graphml_file to have basic compatibility with yEd editor

        :param graphml_file: a graphml file 
      """ 
       
 
      if usetemp==True: 
        f = tempfile.NamedTemporaryFile(delete=False)
        tmpf=f.name
        #warning: issue with cross devide link
      else:
        tmpf=graphml_file+".work.tmp"
        
      tmpf0=tmpf+"0"

      gns='http://graphml.graphdrawing.org/xmlns'
      ns={'x': gns}
      
     
      reptag="yxzzzzxwcvakwwwyyyyxz"
      yns="http://www.yworks.com/xml/graphml"  
      root = et.parse(graphml_file)
      rootel = root.getroot()
      rootel.set("xmlns"+reptag+"y", yns)  

       
      
      child = et.fromstring("<key for=\"node\" id=\"d21\" yfiles.type=\"nodegraphics\"/>")
      rootel.append(child)  
        
      child = et.fromstring("<key for=\"edge\" id=\"d27\" yfiles.type=\"edgegraphics\"/>")
      rootel.append(child)  
         
         
       
              
      root.write(tmpf0,
                 pretty_print=True, xml_declaration=True,
                 encoding='UTF-8')
      f1 = open(tmpf0, "r")
      ofi = open(tmpf, "w")
      fd=0        
      while(True):
          line = f1.readline() 
          if not line:
              break
 
          li=line.strip()
          if fd==0:
            if reptag in li:
                li=li.replace(reptag,":")
                fd=1
          ofi.write(li+"\n")
      ofi.close() 
    
       
      root = et.parse(tmpf)
      
      colors=__color_range()
        
      ns={'x': gns}
      for tag in ["node"]:    
        lst=root.xpath("./x:graph/x:%s" %(tag) , namespaces=ns)
        for elm in lst :
          labeln="" 
          ccode="1"
          for el in elm: 
            
           if el.tag=='{%s}data' %(gns):
            
               ktag="key"
               kv=el.get(ktag)
               if kv=="name":
                    
                  labeln=escape(el.text)
               if kv=="color":
                  ccode=el.text
               if kv=="shape":
                  scode=el.text     
                    
          ncolor=node_shape_to_color(ccode,colors)
          #print("%s %s" %(ccode, ncolor))
          nshape=__node_shape_yed(scode)
          childn = et.fromstring(__yed_node_graphics(labeln,ncolor,nshape))

          elm.append(childn)       
                
      for tag in ["edge"]:    
        lst=root.xpath("./x:graph/x:%s" %(tag) , namespaces=ns)
        for elm in lst :
          labele=""   
          for el in elm: 
            
           if el.tag=='{%s}data' %(gns):
            
               ktag="key"
               kv=el.get(ktag)
               if kv=="spaim":
                    
                  labele=escape(spaim_edge_label(el.text))            
         
        
          
          childe = et.fromstring(__yed_edge_graphics(labele,"#563768"))

          elm.append(childe)   
          
            
      root.write(tmpf,
                 pretty_print=True, xml_declaration=True,
                 encoding='UTF-8')
    
      os.remove(tmpf0)
      shutil.move(tmpf, graphml_file)  



if __name__ == "__main__":
     print("no main defined")








