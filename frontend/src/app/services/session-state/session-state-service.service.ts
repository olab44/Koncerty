import { Injectable } from '@angular/core'
import { BehaviorSubject } from 'rxjs'

@Injectable({
  providedIn: 'root'
})
export class SessionStateServiceService {
  private groupSource = new BehaviorSubject<any>(this.loadFromStorage('group'));
  private eventSource = new BehaviorSubject<any>(this.loadFromStorage('event'));
  currentGroup = this.groupSource.asObservable()
  currentEvent = this.eventSource.asObservable()

  private loadFromStorage(key: string): any {
    const stored = sessionStorage.getItem(key);
    return stored ? JSON.parse(stored) : null;
  }

  setGroup(group: any) {
    sessionStorage.setItem('group', JSON.stringify(group));
    this.groupSource.next(group);
  }

  setEvent(event: any) {
    sessionStorage.setItem('event', JSON.stringify(event));
    this.eventSource.next(event);
  }

  clearStorage() {
    sessionStorage.removeItem('group');
    sessionStorage.removeItem('event');
    this.groupSource.next(null);
    this.eventSource.next(null);
  }
}