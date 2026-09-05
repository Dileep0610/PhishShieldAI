import { useState, useEffect, useRef } from 'react';
import { Html5Qrcode } from 'html5-qrcode';
import './QRScanner.css';

const MAX_QR_URL_LENGTH = 2048;

function validateQRPayload(payload) {
  if (typeof payload !== 'string' || !payload) {
    return { valid: false, type: "UNSUPPORTED_PAYLOAD", reason: "Payload is empty or invalid type" };
  }

  if (payload.length > MAX_QR_URL_LENGTH) {
    return { valid: false, type: "TOO_LONG", reason: `Payload exceeds maximum length of ${MAX_QR_URL_LENGTH} characters` };
  }

  const trimmed = payload.trim();

  // eslint-disable-next-line no-control-regex
  if (/[\x00-\x1F\x7F]/.test(trimmed)) {
    return { valid: false, type: "MALFORMED_PAYLOAD", reason: "Payload contains forbidden control characters" };
  }

  let parsedUrl;
  try {
    parsedUrl = new URL(trimmed);
  } catch {
    return { valid: false, type: "INVALID_URL", reason: "Payload is not a valid URL" };
  }

  if (parsedUrl.protocol !== 'http:' && parsedUrl.protocol !== 'https:') {
    return { valid: false, type: "UNSUPPORTED_SCHEME", reason: "Only HTTP and HTTPS protocols are supported" };
  }

  const hostname = parsedUrl.hostname;
  const isPrivate = /^(localhost|127\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.(1[6-9]|2[0-9]|3[0-1])\.\d+\.\d+)$/.test(hostname);

  if (isPrivate) {
    return { valid: true, type: "SECURITY_WARNING", reason: "URL requires additional security validation (Local/Private IP)", validatedUrl: trimmed };
  }

  return { valid: true, type: "VALID_URL", reason: "Ready for phishing analysis.", validatedUrl: trimmed };
}

export default function QRScanner({ onScan, isScanning, onResetExt }) {
  const [status, setStatus] = useState('IDLE'); // IDLE, DECODING, DECODED, ERROR
  const [decodedPayload, setDecodedPayload] = useState('');
  const [validationResult, setValidationResult] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');
  const html5QrCodeRef = useRef(null);
  const fileInputRef = useRef(null);
  const containerId = "qr-reader";

  const stopCamera = async () => {
    if (html5QrCodeRef.current && html5QrCodeRef.current.isScanning) {
      try {
        await html5QrCodeRef.current.stop();
        html5QrCodeRef.current.clear();
      } catch (err) {
        console.error("Error stopping camera", err);
      }
    }
  };

  useEffect(() => {
    // Cleanup on unmount
    return () => {
      stopCamera();
    };
  }, []);

  const onDecodeSuccess = async (decodedText) => {
    // Prevent duplicate processing
    if (status === 'DECODED') return; 
    
    await stopCamera();
    setDecodedPayload(decodedText);
    setValidationResult(validateQRPayload(decodedText));
    setStatus('DECODED');
  };

  const startCamera = async () => {
    setErrorMsg('');
    setDecodedPayload('');
    setValidationResult(null);
    if (onResetExt) onResetExt();
    
    if (!html5QrCodeRef.current) {
      html5QrCodeRef.current = new Html5Qrcode(containerId);
    }
    
    setStatus('DECODING');
    try {
      await html5QrCodeRef.current.start(
        { facingMode: "environment" },
        { fps: 10, qrbox: { width: 250, height: 250 } },
        onDecodeSuccess,
        () => {
          // Ignore frequent parse errors
        }
      );
    } catch (err) {
      setErrorMsg("Failed to start camera: " + err.message);
      setStatus('ERROR');
      await stopCamera();
    }
  };

  const handleStopCamera = async () => {
    await stopCamera();
    setStatus('IDLE');
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    // Client-side 5MB limit
    if (file.size > 5 * 1024 * 1024) {
      setErrorMsg("File too large. Maximum size is 5 MB.");
      setStatus('ERROR');
      return;
    }
    
    setErrorMsg('');
    setDecodedPayload('');
    setValidationResult(null);
    if (onResetExt) onResetExt();
    setStatus('DECODING');
    await stopCamera();

    if (!html5QrCodeRef.current) {
      html5QrCodeRef.current = new Html5Qrcode(containerId);
    }

    try {
      const decodedText = await html5QrCodeRef.current.scanFile(file, true);
      onDecodeSuccess(decodedText);
    } catch (err) {
      console.error(err);
      setErrorMsg("Failed to decode QR code from image.");
      setStatus('ERROR');
    }
    
    if (fileInputRef.current) {
        fileInputRef.current.value = "";
    }
  };

  const handleReset = () => {
    setDecodedPayload('');
    setValidationResult(null);
    setErrorMsg('');
    setStatus('IDLE');
    if (onResetExt) onResetExt();
  };

  return (
    <div className="qr-scanner">
      {status !== 'DECODED' && (
        <div className="scanner-controls">
            <button 
                onClick={status === 'DECODING' ? handleStopCamera : startCamera} 
                className="scanner-button"
                disabled={isScanning}
            >
                {status === 'DECODING' ? 'Stop Camera' : 'Start Camera'}
            </button>
            <span className="or-divider">OR</span>
            <label className={`scanner-button file-upload-btn ${isScanning ? 'disabled' : ''}`}>
                Upload Image
                <input 
                    type="file" 
                    accept="image/png, image/jpeg, image/webp" 
                    onChange={handleFileUpload} 
                    ref={fileInputRef}
                    className="sr-only"
                    disabled={isScanning}
                />
            </label>
        </div>
      )}
      
      <div 
        id={containerId} 
        className={status === 'DECODING' ? 'qr-reader-active' : 'qr-reader-hidden'}
      ></div>

      {errorMsg && <p className="error-text qr-error" role="alert">{errorMsg}</p>}

      {status === 'DECODED' && (
        <div className="decoded-result">
            <h3 className="evidence-title">Decoded Payload</h3>
            <div className="url-display" style={{ wordBreak: 'break-all', maxHeight: '200px', overflowY: 'auto' }}>
                {decodedPayload}
            </div>

            {validationResult && validationResult.valid ? (
                <div className="validation-success mt-4">
                    <p className="primary-msg">QR code decoded successfully.</p>
                    {validationResult.type === 'SECURITY_WARNING' && (
                        <p className="error-text">⚠️ {validationResult.reason}</p>
                    )}
                    <p className="subtext mt-4">Ready for phishing analysis.</p>
                    <button 
                        className="scanner-button mt-4" 
                        onClick={() => onScan && onScan(validationResult.validatedUrl)}
                        disabled={isScanning}
                    >
                        {isScanning ? 'Analyzing...' : 'Continue to Analysis'}
                    </button>
                </div>
            ) : (
                <div className="validation-error mt-4">
                    <p className="primary-msg" style={{ color: 'var(--danger)' }}>QR code decoded, but the content is not a supported HTTP/HTTPS URL.</p>
                    <p className="error-text">Reason: {validationResult?.reason}</p>
                </div>
            )}

            <div className="mt-4">
                <button onClick={handleReset} className="reset-button" disabled={isScanning}>
                    Scan Again
                </button>
            </div>
        </div>
      )}
    </div>
  );
}
