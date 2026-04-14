import { ReactNode } from 'react';

interface FantasyCardProps {
  children: ReactNode;
  variant?: 'default' | 'gold' | 'red' | 'blue' | 'narrative';
  onClick?: () => void;
}

const variantStyles: Record<string, React.CSSProperties> = {
  default: {
    background: 'linear-gradient(145deg, #1e2945 0%, #151e38 100%)',
    border: '1px solid #2d3755',
  },
  gold: {
    background: 'linear-gradient(145deg, #2a2414 0%, #3d3318 100%)',
    border: '1px solid #d4af37',
  },
  red: {
    background: 'linear-gradient(145deg, #2a1414 0%, #3d1818 100%)',
    border: '1px solid #8b2a2a',
  },
  blue: {
    background: 'linear-gradient(145deg, #142035 0%, #1e2945 100%)',
    border: '1px solid #3b82f6',
    boxShadow: '0 0 10px rgba(59, 130, 246, 0.2)',
  },
  narrative: {
    background: 'linear-gradient(145deg, #0f172a 0%, #1e2945 100%)',
    border: '1px solid #3b82f6',
    boxShadow: 'inset 0 0 20px rgba(59, 130, 246, 0.1)',
  },
};

export function FantasyCard({ children, variant = 'default', onClick }: FantasyCardProps) {
  const baseStyle: React.CSSProperties = {
    borderRadius: '12px',
    padding: '16px',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.4)',
    cursor: onClick ? 'pointer' : 'default',
    transition: 'transform 0.2s, box-shadow 0.2s',
    position: 'relative',
    overflow: 'hidden',
    ...variantStyles[variant],
  };

  return (
    <div
      onClick={onClick}
      style={baseStyle}
      onMouseEnter={(e) => {
        if (onClick) {
          e.currentTarget.style.transform = 'translateY(-2px)';
          e.currentTarget.style.boxShadow = '0 6px 16px rgba(0, 0, 0, 0.5)';
        }
      }}
      onMouseLeave={(e) => {
        if (onClick) {
          e.currentTarget.style.transform = 'translateY(0)';
          e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.4)';
        }
      }}
    >
      {children}
    </div>
  );
}