package LbjTagger;

import java.util.StringTokenizer;
import java.util.Vector;

import lbj.*;

import IO.Keyboard;
import LBJ2.classify.Classifier;
import LBJ2.classify.FeatureVector;
import LBJ2.parse.LinkedVector;

import java.util.Iterator;

import IO.OutFile;
import LBJ2.parse.*;

/**
  * This project was started by Nicholas Rizzolo (rizzolo@uiuc.edu) . 
  * Most of design, development, modeling and
  * coding was done by Lev Ratinov (ratinov2@uiuc.edu).
  * For modeling details and citations, please refer
  * to the paper: 
  * External Knowledge and Non-local Features in Named Entity Recognition
  * by Lev Ratinov and Dan Roth 
  * submitted/to appear/published at NAACL 09.
  * 
 **/

class MyTagger
{
    private NETaggerLevel1 tagger1;
    private NETaggerLevel2 tagger2;

    public MyTagger() {
        tagger1 = new NETaggerLevel1();
        System.out.println("Reading model file : "+ Parameters.pathToModelFile+".level1");
        tagger1=(NETaggerLevel1)Classifier.binaryRead(Parameters.pathToModelFile+".level1");
        tagger2 = new NETaggerLevel2();
        System.out.println("Reading model file : "+ Parameters.pathToModelFile+".level2");
        tagger2=(NETaggerLevel2)Classifier.binaryRead(Parameters.pathToModelFile+".level2");
    }
  
    public void tagFile(String inputFile,String outputFile)
    {
    	System.out.println("Tagging file: "+inputFile);
    	Vector<LinkedVector> data=BracketFileManager.parsePlainText(inputFile);
        NETester.annotateBothLevels(data,tagger1,tagger2);
        
        OutFile out=new OutFile(outputFile);
        for(int i=0;i<data.size();i++){
            LinkedVector vector = data.elementAt(i);
            StringBuffer res=new StringBuffer();
            boolean open=false;
            String[] predictions=new String[vector.size()];
            String[] words=new String[vector.size()];
            for(int j=0;j<vector.size();j++){
            	predictions[j] =   bilou2bio(((NEWord)vector.get(j)).neTypeLevel2);
            	words[j]=((NEWord)vector.get(j)).form;
            }
            for(int j=0;j<vector.size();j++)
            { 
            	if (predictions[j].startsWith("B-")
            			|| 
            			(j>0&&predictions[j].startsWith("I-") && (!predictions[j-1].endsWith(predictions[j].substring(2))))){
            		res.append("[" + predictions[j].substring(2) + " ");
            		open=true;
            	}
            	res.append(words[j]+ " ");
            	if(open){
            		boolean close=false;
            		if(j==vector.size()-1){
            			close=true;
            		}
            		else
            		{
            			if(predictions[j+1].startsWith("B-"))
            				close=true;
            			if(predictions[j+1].equals("O"))
            				close=true;
            			if(predictions[j+1].indexOf('-')>-1&&(!predictions[j].endsWith(predictions[j+1].substring(2))))
            				close=true;
            		}
            		if(close){
            			res.append(" ] ");
            			open=false;
            		}
            	}
            }
            out.println(res.toString());
        }
        out.close();    	
    }
    
    public String bilou2bio(String prediction){
    	if(Parameters.taggingScheme.equalsIgnoreCase(Parameters.BILOU)){
    		if(prediction.startsWith("U-"))
    			prediction="B-"+prediction.substring(2);
    		if(prediction.startsWith("L-"))
    			prediction="I-"+prediction.substring(2);
    	}
    	return prediction;
    }
}


public class Annotator {
	public static void main(String[] args){
        Parameters.readConfigAndLoadExternalData("Config/allLayer1.config");
        Parameters.forceNewSentenceOnLineBreaks=false;
        MyTagger myTagger = new MyTagger();
        System.out.println("Created my tagger");
        for (String file : args) {
            myTagger.tagFile(file, file + "-annotated");
        }
	}
}

