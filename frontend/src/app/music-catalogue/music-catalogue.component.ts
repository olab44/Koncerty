import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { TopBarComponent } from '../bars/top-bar/top-bar.component';
import { OverlayAddCompositionComponent } from '../overlays/overlay-add-composition/overlay-add-composition.component';
import { CompositionInfo, GroupInfo } from '../interfaces';
import { SessionStateService } from '../services/session-state/session-state.service';
import { FilterPipe } from '../pipe/filter.pipe';
import { BackendService } from '../services/backend-connection/backend.service';

@Component({
  selector: 'app-music-catalogue',
  standalone: true,
  imports: [ CommonModule, FormsModule, TranslateModule, TopBarComponent, OverlayAddCompositionComponent, FilterPipe ],
  templateUrl: './music-catalogue.component.html',
  styleUrl: './music-catalogue.component.css'
})
export class MusicCatalogueComponent {
  group!: GroupInfo
  viewedComposition: CompositionInfo | null = null
  visibleOverlayComposition = false
  searchPhrase: string = ""
  compositions: CompositionInfo[] = []
  new_file: File | null = null

  constructor(private backend: BackendService, private state: SessionStateService) {
    this.state.currentGroup.subscribe((group) => {
      this.group = group;
    });
    this.getCatalogue()
  }

  getCatalogue() {
    this.backend.getCatalogueExtra(this.group.group_id).subscribe({
      next: (res) => {this.compositions = res.found},
      error: (e) => { console.log(e) }
    })
  }

  viewComposition(composition: CompositionInfo): void {
    this.viewedComposition = composition;
    console.log('Viewed Composition ID:', this.viewedComposition?.id);
  }
  
  removeComposition(event: MouseEvent, id: number): void {
    event.stopPropagation()
    this.backend.deleteRequest('catalogue/removeComposition', {composition_id: id, parent_group: this.group.group_id}).subscribe({
      next: (res) => { console.log(res); this.getCatalogue() },
      error: (e) => { console.log(e) }
    })
  }

  downloadFile(file_id: number): void {
    this.backend.postRequest('files/downloadFile', {file_id, parent_group: this.group.group_id}).subscribe({
      next: (res) => { console.log(res) },
      error: (e) => { console.log(e) }
    })
  }

  deleteFile(file_id: number): void {
    this.backend.deleteRequest('files/deleteFile', {file_id, parent_group: this.group.group_id}).subscribe({
      next: (res) => {
        if (this.viewedComposition) {
          this.viewedComposition.files = this.viewedComposition?.files.filter(file => file.id !== file_id)
        }
      },
      error: (e) => { console.log(e) }
    })
  }

  onFileChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.new_file = input.files[0]
    }
  }


  uploadFile(): void {
    if (!this.new_file) {
      console.log('No file selected');
      return;
    }
  
    const formData = new FormData();
    formData.append('file', this.new_file, this.new_file.name);
    formData.append('file_name', this.new_file.name);
    formData.append('parent_group', this.group.group_id.toString());
  
    this.backend.postRequest('files/uploadFile', formData).subscribe({
      next: (res: any) => {
        const createdFile = res.created_file;
        if (!createdFile || !createdFile.file_id) {
          console.error('File ID missing from response');
          return;
        }

        if (this.viewedComposition?.id) {
          const fileData = {
            file_id: createdFile.file_id,
            composition_id: this.viewedComposition.id,
            parent_group: this.group.group_id
          };
          this.backend.postRequest('files/assignFileToComposition', fileData).subscribe({
            next: (assignRes: any) => {
              console.log('File assigned to composition:', assignRes);
              this.getCatalogue();
            },
            error: (assignError) => {
              console.error('Error assigning file to composition:', assignError);
            }
          });
        } else {
          console.error('No composition selected or composition ID is missing');
        }
      },
      error: (uploadError) => {
        console.log('Error uploading file:', uploadError);
      }
    });
  
    this.new_file = null;
  }

  toggleOverlayComposition(): void {
    this.visibleOverlayComposition = !this.visibleOverlayComposition
  }
}
