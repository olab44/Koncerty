import { Component, EventEmitter, Output } from '@angular/core';
import { TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-overlay-join-group',
  standalone: true,
  imports: [TranslateModule],
  templateUrl: './overlay-join-group.component.html',
  styleUrl: './overlay-join-group.component.css'
})
export class OverlayJoinGroupComponent {
  @Output() close = new EventEmitter<void>()

  joinMessage: string = '...'

  validateCode(groupCode: string) : boolean {
    return groupCode !== ""
  }

  joinGroup(groupCode: string) : void {
    // TODO: API CALL
    this.joinMessage = this.validateCode(groupCode) ? "<<group joining status>>" : "Please, input the valid code."
  }

  closeOverlay() {
    this.close.emit()
  }
}
