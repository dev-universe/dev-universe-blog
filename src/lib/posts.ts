import { getCollection } from 'astro:content';
export const posts = async () => (await getCollection('posts')).filter(p => !p.data.draft).sort((a,b) => b.data.date.valueOf()-a.data.date.valueOf() || a.id.localeCompare(b.id));
export const date = (d: Date) => d.toISOString().slice(0,10).replaceAll('-', '.');
export const minutes = (body: string='') => Math.max(1, Math.ceil(body.length/700));
