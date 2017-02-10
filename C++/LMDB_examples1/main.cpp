#include <string.h>  
#include <stdlib.h>  
#include <iostream>  
#include <stdio.h>
#include <string>  
#include <lmdb.h>
using namespace std;
const char *pMdbFilePath = "./MdbFile";  
class Mdb{
	private:  
	    MDB_env *env;  
	    MDB_txn *txn;  
	    MDB_dbi dbi;  
	    MDB_cursor *cursor; 
	public:  
	    Mdb(){  
	        cout << "Im Mdb Constuctor" << endl;  
	    }  
	    ~Mdb(){  
	        cout << "Im Desructor" << endl;  
	    }  
	    bool InitMdbEnv(const char *pMdbFile, int nSize){
	    	int rc = mdb_env_create(&env);
	    	if(rc) { cout << "create env Fialed!!!" << endl; return false; }  
	    	rc= mdb_env_set_mapsize(env, nSize);
	    	if(rc) { cout << "create mapsize Fialed!!!" << endl; return false; }  
	    	rc = mdb_env_open(env, pMdbFile, 0, 0664);  //0664 is the authorization right; directory must exsit at first
		    if(rc) { cout << rc<<"\t"<<"Initialize " << pMdbFile << "Mdb Fialed!!!" << endl; return false; }  
		    return true;  
	    }
	    bool MdbTxnBegin(){  
		    if(mdb_txn_begin(env, NULL, 0, &txn)) {cout << "mdb_open failed!!!" << endl; return false;}  
		    return true;  
		}  
	    bool MdbOpen(){  
		    if(mdb_open(txn, NULL, 0, &dbi)) {cout << "mdb_txn_beginfailed!!!" << endl; return false;}  
		    return true;  
		}
		bool MdbPut(char* pKey, char* pData)  
		{  
		    MDB_val key, data;  
		    key.mv_size = strlen(pKey)+1;  
		    key.mv_data = pKey;  
		    data.mv_size = strlen(pData)+1;  
		    data.mv_data = pData;  
		    int rc = mdb_put(txn, dbi, &key, &data, MDB_NOOVERWRITE);  
		    if(rc == MDB_MAP_FULL) { cout << "Mdb File is full, Alert!!!" << endl; return false; }  
		    return true;  
		} 
		bool MdbTxnCommit(){  
		    if(mdb_txn_commit(txn)) { cout << "mdb_txn_commit failed" << endl; return false; }  
		    return true;  
		} 
		bool MdbCursorOpen(){  
		    if(mdb_cursor_open(txn, dbi, &cursor)) { cout << "mdb_cursor_open Failed!!!" << endl; return false; }  
		    return true;  
		}
		void MdbCursorClose(){  
		    mdb_cursor_close(cursor);  
		    return ;  
		}
		void MdbTxnAbort(){  
		    mdb_txn_abort(txn);  
		    return ;  
		} 
		bool MdbCursorPut(char* pKey, char* pData){  
		    MDB_val key, data;  
		    key.mv_size = strlen(pKey)+1;  
		    key.mv_data = pKey;  
		    data.mv_size = strlen(pData)+1;  
		    data.mv_data = pData;  
		    if(mdb_cursor_put(cursor, &key, &data, MDB_NODUPDATA)) { cout << "MdbCursorPut Failed!!!" <<endl; return false; }  
		    return true;  
		}  
		bool MdbCursorGet(char* pKey, char *pData){  
		    MDB_val key, data;  
		    key.mv_size = strlen(pKey)+1;  
		    key.mv_data = pKey;  
		    if(mdb_cursor_get(cursor, &key, &data, MDB_NEXT)) { cout << "mdb_cursor_get Failed Or No Data!!!" <<endl; return false; }  
		    strcpy(pData, (char*)data.mv_data);  
		    strcpy(pKey, (char*)key.mv_data);  
		    return true;  
		} 
		bool MdbGet(char* pKey, char* pData){  
		    MDB_val key, data;  
		    key.mv_size = strlen(pKey)+1;  
		    key.mv_data = pKey;  
		    if(mdb_get(txn, dbi, &key, &data)) { cout << "mdb_get failed!!!" << endl; return false; }  
		    strcpy(pData, (char*)data.mv_data);  
		    return true;  
		}  
		void MdbClose(){  
		    mdb_close(env, dbi);  
		    return ;  
		}  
		void MdbEnvClose(){  
		    mdb_env_close(env);  
		    return ;  
		}  

};
int main(int argc,char *argv[])  
{  
    Mdb mdb;    //Create a Mdb Objiect  
    mdb.InitMdbEnv(pMdbFilePath, 200*1024*1024);//Initialize Mdb Env and Specifc Mdb File Max Size 
   
    //************mdb_put Restore Data*******************
    mdb.MdbTxnBegin();  //Begin a Transition  
    mdb.MdbOpen();      //Open a Mdb File  
    char cKey[10]="";  
    char cValue[100]="Im value";  
    for(int i=0; i<10; i++) { 
        sprintf(cKey, "%06d", i);  
        mdb.MdbPut(cKey, cValue);   //mdb_put Restore Data  
    }  
    mdb.MdbTxnCommit();   //Commit Transition  
    //*****************************************************  
    //************mdb_get Get items Form Database**********  
    char cKey1[]="000002";  
    char cValue1[100]="";  
    mdb.MdbTxnBegin();  
    mdb.MdbGet(cKey1, cValue1);  
    mdb.MdbTxnCommit();  
    cout << "Key:000002:" << cValue1 << endl;  
    //*****************************************************  
     
    //************mdb_cursor_put Using Cursor Restore Data*******  
    char cKey2[10]="";  
    char cValue2[100]="I m Cursor Values";  
    mdb.MdbTxnBegin();  
    mdb.MdbCursorOpen();  
    for(int i=10; i<20; i++) {  
        sprintf(cKey2, "%06d", i);  
        mdb.MdbCursorPut(cKey2, cValue2);  
    }  
    mdb.MdbCursorClose();  
    mdb.MdbTxnCommit();  
    //***********************************************************  
      
    //***********mdb_cursor_get Using Cursor Get Data************  
    mdb.MdbTxnBegin();  
    mdb.MdbCursorOpen();  
    char cKey3[10]="";  
    char cValue3[100]="";  
    while (mdb.MdbCursorGet(cKey3, cValue3)) {  
        cout << "Key: " << cKey3 << "    data: " << cValue3 << endl;  
    }
    mdb.MdbCursorClose();  
    mdb.MdbTxnAbort();  
    //***********************************************************  
    
    mdb.MdbClose(); //Close Mdb File  
    mdb.MdbEnvClose();  //Close Mdb Env  
    return 0;  
}  