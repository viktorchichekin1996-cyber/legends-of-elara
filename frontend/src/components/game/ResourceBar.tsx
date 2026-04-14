import { Text } from '@vkontakte/vkui';
import { ReactNode } from 'react';

interface ResourceBarProps {
  label: string;
  value: number;
  max: number;
  color?: 'red' | 'blue' | 'green' | 'orange' | 'purple';
  icon?: ReactNode;
}

const colorMap: Record<string, string> = {
  red: 'var(--vkui--color_accent_red)',
  blue: 'var(--vkui--color_accent_blue)',
  green: 'var(--vkui--color_accent_green)',
  orange: 'var(--vkui--color_accent_orange)',
  purple: 'var(--vkui--color_accent_purple)',
};

export function ResourceBar({ label, value, max, color = 'green', icon }: ResourceBarProps) {
  const percentage = max > 0 ? (value / max) * 100 : 0;
  const barColor = colorMap[color];

  return (
    <div style={{ marginBottom: 8 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
          {icon}
          <Text weight="2" style={{ fontSize: 13 }}>
            {label}
          </Text>
        </div>
        <Text style={{ fontSize: 13, color: 'var(--vkui--color_text_secondary)' }}>
          {value} / {max}
        </Text>
      </div>
      <div style={{ position: 'relative', height: 8, borderRadius: 4, background: 'var(--vkui--color_image_border_alpha)' }}>
        <div
          style={{
            position: 'absolute',
            left: 0,
            top: 0,
            height: '100%',
            width: `${percentage}%`,
            borderRadius: 4,
            background: barColor,
            transition: 'width 0.3s ease',
          }}
        />
      </div>
    </div>
  );
}