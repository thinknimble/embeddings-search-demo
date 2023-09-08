import { computed } from 'vue'
export function useModelWrapper(props, emit, name = 'modelValue') {
  /**
   * Unwrap model value into component
   * Remember to also add emitter to emits in component definitiion
   * emits:['update:<name>']
   */
  return computed({
    get: () => props[name],
    set: (value) => emit(`update:${name}`, value),
  })
}
