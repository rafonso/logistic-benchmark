import { IParameters } from '../parameters/IParameters';

export interface Action {
  run(params: IParameters): void;
}