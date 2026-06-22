import { Component } from 'react';

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, info) {
    console.error('[ErrorBoundary] Caught error:', error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ maxWidth:'600px', margin:'60px auto', padding:'32px', background:'#fce8e6', borderRadius:'10px', textAlign:'center' }}>
          <h2 style={{ color:'#c5221f', marginBottom:'16px' }}>Something went wrong</h2>
          <p style={{ color:'#555', marginBottom:'20px' }}>{this.state.error?.message || 'An unexpected error occurred.'}</p>
          <button onClick={() => this.setState({ hasError:false, error:null })} style={{ padding:'10px 24px', background:'#1a73e8', color:'white', border:'none', borderRadius:'6px', cursor:'pointer' }}>
            Try Again
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

export default ErrorBoundary;