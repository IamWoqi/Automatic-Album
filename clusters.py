#coding=utf-8;
import SimilarityAlgorithm as sa;
from bicluster import Bicluster;

def readfile(filename):
	lines = [line for line in open(filename)];
	
	#��һ�����б��⣺(�����б�)
	colnames = lines[0].strip().split('\t')[1:];
	#��ŵ�һ�У�(�������б�)
	rownames = [];
	#�������(ÿƪ���͵ĵ���Ƶ��)
	data = [];
	
	for line in lines[1:]:
		p = line.strip().split('\t');
		rownames.append(p[0]);
		data.append([float(x) for x in p[1:]]);
		
	return rownames,colnames,data;
	
def hcluster(rows,distance = sa.pearson):
	distances = {};
	currentclustid = -1;
	
	#�ʼ�ľ��������ݼ��е���
	clust = [Bicluster(rows[i],id = i) for i in range(len(rows))]; 
	
	while len(clust)>1:
		#��ض�����ܵ�һ�����
		lowestpair = (0,1);
		#����������ض�
		closest = distance(clust[0].vec,clust[1].vec);
		
		#����ÿһ����ԣ�Ѱ����С����
		for i in range(len(clust)):
			for j in range(i+1,len(clust)):
				#��distances���������ļ���ֵ
				if(clust[i].id,clust[j].id not in distances):
					distances[(clust[i].id,clust[j].id)] = distance(clust[i].vec,clust[j].vec);
				d = distances[(clust[i].id,clust[j].id)];
				if(d < closest):
					closest = d;
					lowestpair = (i,j);
		
		#������������������ƽ��ֵ
		mergevec = [clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]/2.0 
		for i in range(len(clust[0].vec))];
		
		#�����µľ���,IDΪ��������ʾ�������ɵľ���
		newcluster = Bicluster(mergevec,left = clust[lowestpair[0]],
							   right = clust[lowestpair[1]],
							   distance = closest,id = currentclustid);
		
		#ɾ���ѱ��ϲ��ľ���,ԭ�о��༯�������ϲ���ľ���
		currentclustid -= 1;
		del clust[lowestpair[1]];
		del clust[lowestpair[0]];
		clust.append(newcluster);
		
	return clust[0];

def printclust(clust,labels = None,n = 25):
	#���������������㼶����
	for i in range(n): print(" ",end="");
	if(clust.id <0):
		#"oo"��ʾ�þ�����һ����֧
		print("oo");
	else:
		#���������þ�����һ��Ҷ�ӽڵ�
		if labels == None: return ;
		else : print(labels[clust.id]);
	
	#������������
	if clust.left != None:
		printclust(clust.left,labels = labels , n = n-1);
	if clust.right != None:
		printclust(clust.right,labels = labels , n = n+1);
	

writersname,wordsname,wordscount = readfile("blogdata.txt");
clust = hcluster(wordscount);
printclust(clust,writersname);
