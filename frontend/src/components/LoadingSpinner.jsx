import React from 'react';

const LoadingSpinner = () => (
  <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 80 }}>
    <div className="spinner" style={{
      border: '4px solid #1f2933',
      borderTop: '4px solid #3b82f6',
      borderRadius: '50%',
      width: 36,
      height: 36,
      animation: 'spin 1s linear infinite',
    }} />
    <style>{`
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    `}</style>
  </div>
);

export default LoadingSpinner;
