const PREFIX = 'elara:';

export const localStorageUtil = {
  get<T>(key: string): T | null {
    try {
      const item = localStorage.getItem(`${PREFIX}${key}`);
      if (!item) return null;
      return JSON.parse(item) as T;
    } catch (err) {
      console.error(`localStorage get error for ${key}:`, err);
      return null;
    }
  },

  set<T>(key: string, value: T): void {
    try {
      localStorage.setItem(`${PREFIX}${key}`, JSON.stringify(value));
    } catch (err) {
      console.error(`localStorage set error for ${key}:`, err);
    }
  },

  remove(key: string): void {
    try {
      localStorage.removeItem(`${PREFIX}${key}`);
    } catch (err) {
      console.error(`localStorage remove error for ${key}:`, err);
    }
  },

  clear(): void {
    try {
      Object.keys(localStorage)
        .filter((k) => k.startsWith(PREFIX))
        .forEach((k) => localStorage.removeItem(k));
    } catch (err) {
      console.error('localStorage clear error:', err);
    }
  },
};