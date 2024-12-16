import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-overlay-join-group',
  standalone: true,
  imports: [],
  templateUrl: './overlay-join-group.component.html',
  styleUrl: './overlay-join-group.component.css'
})
export class OverlayJoinGroupComponent {
  @Output() close = new EventEmitter<void>()

  joinMessage: string = ''

  validateCode(groupCode: string) : boolean {
    return true
  }

  joinGroup(groupCode: string) : void {
    if (this.validateCode(groupCode)) {
      // do stuff
    }
  }

  closeOverlay() {
    this.close.emit()
  }
}
