import React from 'react';
import { ImageResponse } from '@vercel/og';

export const config = { runtime: 'edge' };

export default function handler() {
  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          background: '#fff8f2',
          color: '#241f2a',
          padding: '64px 76px',
          position: 'relative',
          overflow: 'hidden',
          fontFamily: 'sans-serif',
        }}
      >
        <div style={{position:'absolute',width:320,height:320,borderRadius:320,background:'#ffd6df',top:-145,left:-105,display:'flex'}} />
        <div style={{position:'absolute',width:300,height:300,borderRadius:300,background:'#d9f2ee',right:-95,bottom:-145,display:'flex'}} />

        <div style={{display:'flex',alignItems:'center',gap:20,zIndex:2}}>
          <div style={{width:68,height:68,borderRadius:20,background:'#ff8ea3',display:'flex',alignItems:'center',justifyContent:'center',fontSize:38,fontWeight:900}}>N</div>
          <div style={{display:'flex',flexDirection:'column'}}>
            <div style={{fontSize:34,fontWeight:900}}>Name the Baby</div>
            <div style={{fontSize:19,color:'#716978',marginTop:3}}>namethebaby.site</div>
          </div>
        </div>

        <div style={{display:'flex',flexDirection:'column',zIndex:2,maxWidth:980}}>
          <div style={{fontSize:76,fontWeight:900,lineHeight:1.02,letterSpacing:-3}}>Find it. Build it. Vote on it.</div>
          <div style={{fontSize:29,lineHeight:1.35,color:'#5f5664',marginTop:24}}>Explore 1,500+ baby names, create something new, save your favorites, and let family vote live.</div>
        </div>

        <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',zIndex:2}}>
          <div style={{display:'flex',gap:14}}>
            <div style={{border:'2px solid #eaded7',background:'#fffdfb',borderRadius:999,padding:'12px 19px',fontSize:18,fontWeight:800,display:'flex'}}>1,500+ names</div>
            <div style={{border:'2px solid #eaded7',background:'#fffdfb',borderRadius:999,padding:'12px 19px',fontSize:18,fontWeight:800,display:'flex'}}>Name Creation Lab</div>
            <div style={{border:'2px solid #eaded7',background:'#fffdfb',borderRadius:999,padding:'12px 19px',fontSize:18,fontWeight:800,display:'flex'}}>Live family voting</div>
          </div>
          <div style={{fontSize:18,fontWeight:800,color:'#716978'}}>No account required</div>
        </div>
      </div>
    ),
    { width: 1200, height: 630 },
  );
}
