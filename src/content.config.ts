import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';
export const collections = { posts: defineCollection({ loader: glob({ pattern: '**/*.md', base: './src/content/posts' }), schema: z.object({ title: z.string(), description: z.string(), date: z.coerce.date(), updated: z.coerce.date().optional(), summary: z.string(), category: z.string(), tags: z.array(z.string()), draft: z.boolean().default(false) }) }) };
