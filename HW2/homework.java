//package hwtrial;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
//package hwtrial;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.util.ArrayList;
import java.util.*;
/**
 *
 * @author Prerna
 */
public class homework {
    public static void main(String args[]) throws IOException{
        ArrayList<String>lines=new ArrayList<String>();
        BufferedReader in = new BufferedReader(new FileReader("input.txt"));
        String str;
        while((str=in.readLine()) != null){
            lines.add(str);
        }
        
        int n=Integer.parseInt(lines.get(0));
        String atype=lines.get(1);
        String current_player=lines.get(2);
        int max_depth=Integer.parseInt(lines.get(3));
             
        //read the board
        int board[][]=new int[n][n];
        for(int i=4; i< 4+n; i++)
        {
            String line[]=lines.get(i).split(" ");
            for(int j=0; j<n; j++){
                board[i-4][j]=Integer.parseInt(line[j]);
            }
        }
        //read the initial state
        String state="";
        for(int i=4+n; i< 4+n+n; i++){
            String line=lines.get(i);
            state+=line;
        }
        Writer writer = new BufferedWriter(new OutputStreamWriter(
              new FileOutputStream("correct_output.txt"), "utf-8"));
        //create initial object
        BoardState bs=new BoardState(0,state,null, "Start",current_player);
        String ans[];
        if(atype.equals("MINIMAX"))
            ans=bs.minimax(n, max_depth, board, current_player);
        else
            ans=bs.alphabeta(n, max_depth, board, current_player);
        writer.write(ans[1]+"\n");
        for(int i=0; i<n*n; i+=n)
        {    if(i==n*n-1)
                writer.write(ans[0].substring(i,i+n));
            else
                writer.write(ans[0].substring(i,i+n)+"\n");
        }
        writer.close();
    }   
}
class BoardState{
    int depth, x_score, o_score;
    String state, move;
    char now_play, opponent;
    BoardState parent;
    public BoardState(int depth, String state, BoardState parent, String move, String now_play){
        this.depth=depth;
        this.state=state;
        this.parent=parent;
        this.move=move;
        this.now_play=now_play.charAt(0);
        switch(this.now_play){
            case 'X':
                this.opponent='O';
                break;
            case 'O':
                this.opponent='X';
                break;
        }
        this.x_score=0;
        this.o_score=0;
    }
    public int get_score(int board[][], int n, String current_player){
        for(int i=0; i<n; i++){
            for(int j=0; j<n; j++){
                if(this.state.charAt(i*n+j)=='X')
                    this.x_score+=board[i][j];
                else if(this.state.charAt(i*n+j)=='O')
                    this.o_score+=board[i][j];
            }      
        }
        if(current_player.equals("X"))
            return this.x_score-this.o_score;
        else
            return this.o_score-this.x_score;
    }
    public String[] stake(int i, int j, int n){
        String ans[]= new String[2];
        if(i>=0 && j>=0 && i<n && j<n){
            if(this.state.charAt(n*i+j)=='.'){
                StringBuilder sb= new StringBuilder(this.state);
                sb.setCharAt(n*i+j, this.now_play);
                String news=sb.toString();
                char col=(char)(65+j);
                int row=i+1;
                String move=Character.toString(col)+Integer.toString(row)+" "+"Stake";
                ans[0]=news;
                ans[1]=move;                 
            }
        }
        return ans;    
    }
    public ArrayList<String []> can_stake(int n){
        ArrayList<String []> ans=new ArrayList<>();
        for(int i=0; i<n; i++){
            for(int j=0; j<n; j++){
                String a[]=this.stake(i, j, n);
                if(a[0]==null && a[1]==null)
                    continue;
                else
                    ans.add(a);
            }
        }   
        return ans;    
    }
    public String raid_neighbors(int newr, int newc, int n, String news){
        StringBuilder sb=new StringBuilder(news);
        int conr, conc;
        //check up
        conr=newr-1;
        conc=newc;
        if(conr>=0 && news.charAt(n*conr+conc)==this.opponent)
            sb.setCharAt(n*conr+conc, this.now_play);
        //check left
        conr=newr;
        conc=newc-1;
        if(conc>=0 && news.charAt(n*conr+conc)==this.opponent)
            sb.setCharAt(n*conr+conc, this.now_play);
        //check right
        conr=newr;
        conc=newc+1;
        if(conc < n &&news.charAt(n*conr+conc)==this.opponent)
            sb.setCharAt(n*conr+conc, this.now_play);
        //check down
        conr=newr+1;
        conc=newc;
        if(conr <n && news.charAt(n*conr+conc)==this.opponent)
            sb.setCharAt(n*conr+conc, this.now_play);
        
        return sb.toString();
    }
    public ArrayList<String []> can_raid(int n){
        ArrayList<String []> ans=new ArrayList<>();
        for(int i=0; i<n; i++){
            for(int j=0; j<n; j++){
                //check if current player exists in square
                if(this.state.charAt(i*n+j)==this.now_play){
                    //check if empty squares nearby
                    int newr, newc;
                    //check up
                    newr=i-1;
                    newc=j;
                    if(newr>=0 && this.state.charAt(newr*n+newc)=='.'){
                        String a[]=new String[2];
                        StringBuilder sb=new StringBuilder(this.state);
                        sb.setCharAt(newr*n+newc,this.now_play);
                        char col=(char)(65+newc);
                        int row=newr+1;
                        String move_name=Character.toString(col)+Integer.toString(row)+" "+"Raid";
                        String new_state=this.raid_neighbors(newr, newc, n, sb.toString());
                        a[0]=new_state;
                        a[1]=move_name;
                        //System.out.println(move_name);
                        ans.add(a);  
                        //System.out.println(ans);
                    }
                    //check left
                    newr=i;
                    newc=j-1;
                    if(newc>=0 && this.state.charAt(newr*n+newc)=='.'){
                        String a[]=new String[2];
                        StringBuilder sb=new StringBuilder(this.state);
                        sb.setCharAt(newr*n+newc,this.now_play);
                        char col=(char)(65+newc);
                        int row=newr+1;
                        String move_name=Character.toString(col)+Integer.toString(row)+" "+"Raid";
                        String new_state=this.raid_neighbors(newr, newc, n, sb.toString());
                        a[0]=new_state;
                        a[1]=move_name;
                        //System.out.println(move_name);
                        ans.add(a);      
                        //System.out.println(ans);
                    }
                    //check right
                    newr=i;
                    newc=j+1;
                    if(newc< n && this.state.charAt(newr*n+newc)=='.'){
                        String a[]=new String[2];
                        StringBuilder sb=new StringBuilder(this.state);
                        sb.setCharAt(newr*n+newc,this.now_play);
                        char col=(char)(65+newc);
                        int row=newr+1;
                        String move_name=Character.toString(col)+Integer.toString(row)+" "+"Raid";
                        String new_state=this.raid_neighbors(newr, newc, n, sb.toString());
                        a[0]=new_state;
                        a[1]=move_name;
                        //System.out.println(move_name);
                        ans.add(a);     
                        //System.out.println(ans);
                    }
                    //check down
                    newr=i+1;
                    newc=j;
                    if(newr< n && this.state.charAt(newr*n+newc)=='.'){
                        String a[]=new String[2];
                        StringBuilder sb=new StringBuilder(this.state);
                        sb.setCharAt(newr*n+newc,this.now_play);
                        char col=(char)(65+newc);
                        int row=newr+1;
                        String move_name=Character.toString(col)+Integer.toString(row)+" "+"Raid";
                        String new_state=this.raid_neighbors(newr, newc, n, sb.toString());
                        a[0]=new_state;
                        a[1]=move_name;
                        //System.out.println(move_name);
                        ans.add(a);  
                        //System.out.println(ans);
                    }
                }
            }
        }
        return ans;
    }
    public ArrayList<BoardState> get_children(int n, int limit){
        ArrayList<BoardState> children=new ArrayList<>();
        if(this.depth!= limit){
            ArrayList<String []> nexts=new ArrayList<>();
            nexts.addAll(this.can_stake(n));
            nexts.addAll(this.can_raid(n));
            Iterator<String []> iterator=nexts.iterator();
            while(iterator.hasNext()){
                String pp[]=iterator.next();
                BoardState c= new BoardState(this.depth+1, pp[0],this, pp[1], Character.toString(this.opponent));
                children.add(c);    
                //System.out.println(c.get_score());
            }
        }    
        return children;
    }
    public int find_min(int board[][], int limit, int n, String current_player){
        ArrayList<BoardState> children= new ArrayList<>(this.get_children(n, limit));
        if(this.depth== limit || children.isEmpty()){
            int v= this.get_score(board, n, current_player);
            return v;
        }
        else{
            int v= Integer.MAX_VALUE;
            Iterator<BoardState> iterator= children.iterator();
            while(iterator.hasNext()){
                BoardState b= iterator.next();
                v=Math.min(v, b.find_max(board, limit, n, current_player));
            }
            return v;
        }
    }
    public int find_max(int board[][], int limit, int n, String current_player){
        ArrayList<BoardState> children= new ArrayList<>(this.get_children(n, limit));
        if(this.depth== limit || children.isEmpty()){
            int v= this.get_score(board, n, current_player);
            return v;
        }
        else{
            int v= -Integer.MAX_VALUE;
            Iterator<BoardState> iterator= children.iterator();
            while(iterator.hasNext()){
                BoardState b= iterator.next();
                v=Math.max(v, b.find_min(board, limit, n, current_player));
            }
            return v;
        }
    }
    public String[] minimax(int n, int limit, int board[][], String current_player){
        String ans[]= new String[2];
        ArrayList<BoardState> children= new ArrayList<>(this.get_children(n, limit));
        Iterator<BoardState> iterator= children.iterator();
        int v=-Integer.MAX_VALUE;
        while(iterator.hasNext()){
            BoardState x= iterator.next();
            int i=x.find_min(board, limit, n, current_player);
            if(v<i){
                ans[0]=x.state;
                ans[1]=x.move;
                v=i;                      
            }
        }
        return ans;
    } 
    public String[] alphabeta(int n, int limit, int board[][], String current_player){
        String ans[]= new String[2];
        ArrayList<BoardState> children= new ArrayList<>(this.get_children(n, limit));
        Iterator<BoardState> iterator= children.iterator();
        int v=-Integer.MAX_VALUE;
        while(iterator.hasNext()){
            BoardState x= iterator.next();
            int i=x.ab_find_min(board, limit, n, current_player, -Integer.MAX_VALUE, Integer.MAX_VALUE);
            if(v<i){
                ans[0]=x.state;
                ans[1]=x.move;
                v=i;                      
            }
        }
        return ans;
    }
    public int ab_find_max(int board[][], int limit, int n, String current_player, int alpha, int beta){
        ArrayList<BoardState> children= new ArrayList<>(this.get_children(n, limit));
        if(this.depth==limit || children.isEmpty()){
            int v= this.get_score(board, n, current_player);
            return v;
        }
        else{
            int v=-Integer.MAX_VALUE;
            Iterator<BoardState> iterator= children.iterator();
            while(iterator.hasNext()){
                BoardState x=iterator.next();
                v=Math.max(v,x.ab_find_min(board, limit, n, current_player, alpha, beta));
                if(v>=beta)
                    return v;
                alpha=Math.max(v,alpha);         
            }
            return v; 
        }    
    }
    public int ab_find_min(int board[][], int limit, int n, String current_player, int alpha, int beta){
        ArrayList<BoardState> children= new ArrayList<>(this.get_children(n, limit));
        if(this.depth==limit || children.isEmpty()){
            int v= this.get_score(board, n, current_player);
            return v;
        }
        else{
            int v=Integer.MAX_VALUE;
            Iterator<BoardState> iterator= children.iterator();
            while(iterator.hasNext()){
                BoardState x=iterator.next();
                v=Math.min(v,x.ab_find_max(board, limit, n, current_player, alpha, beta));
                if(v<=alpha)
                    return v;
                beta=Math.min(v,beta);         
            }
            return v; 
        }       
    }
}