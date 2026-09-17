import { useEffect, useState } from 'react';

export const useMediaQuery = (query) => {
  const [coincide, setCoincide] = useState(() =>
    typeof window !== 'undefined' ? window.matchMedia(query).matches : false
  );

  useEffect(() => {
    const mql = window.matchMedia(query);
    const onChange = (e) => setCoincide(e.matches);
    setCoincide(mql.matches);
    mql.addEventListener('change', onChange);
    return () => mql.removeEventListener('change', onChange);
  }, [query]);

  return coincide;
};