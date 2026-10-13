import rss from '@astrojs/rss';
import { posts } from '../lib/posts';
export async function GET(context){return rss({title:'DEV UNIVERSE',description:'universe의 기술 기록',site:context.site,items:(await posts()).map(p=>({title:p.data.title,description:p.data.description,pubDate:p.data.date,link:'/posts/'+p.id+'/'})),customData:'<language>ko</language>'})}
