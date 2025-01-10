import { Pipe, PipeTransform } from '@angular/core';
import { TranslationService } from '../services/translation/translation.service';

@Pipe({
  name: 'filterPipe',
  standalone: true
})
export class FilterPipe implements PipeTransform {
  constructor(private translatation: TranslationService) {}

  transform(items: any[], mode: string, searchPhrase: string): any[] {
    if (!items) return [];

    switch (mode) {
      case 'email':
        if (!searchPhrase) return items;
        return items.filter(item => item.email.toLowerCase().includes(searchPhrase.toLowerCase()));
      case 'role':
          if (!searchPhrase) return items;
          return items.filter(item => this.translatation.translate.instant(`MEMBER.${item.role}`).toLowerCase().includes(searchPhrase.toLowerCase()));
      case 'title':
        if (!searchPhrase) return items;
        return items.filter(item => item.title.toLowerCase().includes(searchPhrase.toLowerCase()));
      default:
        return items;
    }
  }
}